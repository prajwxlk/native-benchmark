"""Run benchmark trials: (model x arm x question x run) through OpenCode, headless.

Each trial gets its own isolated OpenCode config/data dirs (XDG_*), so your own
OpenCode setup, plugins and credentials never leak in. The OpenAI key is read from
OPENAI_API_KEY in the environment or from the project's .env file; it is never printed.

  python3 -I bench/run.py --models gpt-5-mini --arms markdown native --questions F01 L01 --runs 1
  python3 -I bench/run.py --budget 9.90 ...      # stops before total spend passes this

Results append to results/trials.jsonl; finished trials are skipped on rerun.
"""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results" / "trials.jsonl"
NATIVE_BIN = ROOT / "vendor/native/target/debug/mcp-stdio"
NATIVE_DB = DATA / "native.db"
TAG = ""  # set by --tag; prefixes trial ids so corpora never collide
PRICES = json.loads((ROOT / "bench/prices.json").read_text()) if (ROOT / "bench/prices.json").exists() else {}

PROMPT = {
    "markdown": "You are answering a question about the company Fernwork, using only its notes. "
                "The notes are Markdown files (with [[wikilinks]]) in the folder ./vault in your working directory. "
                "Use your tools to search and read them.",
    "native": "You are answering a question about the company Fernwork, using only its notes. "
              "The notes are in a Native workspace, available to you through the `native` MCP tools. "
              "Use those tools to search and read them.",
    # Same tools as "native", plus a short hint that emulates the product-side fixes we suggest
    # (slim orientation, forgiving search scope, surfacing the superseded-by recipe).
    "native_hinted": "You are answering a question about the company Fernwork, using only its notes. "
                     "The notes are in a Native workspace, available to you through the `native` MCP tools. "
                     "Tips: you do not need to call bootstrap. Search with records_read operation 'search' and "
                     "arguments {query} only (scope is a record id, so omit it). A newer record that replaces an "
                     "older one has a link with relationship 'supersedes' (see sql_read query_sql on the links "
                     "and records tables). get_record payloads are large, so fetch only records you need.",
}
SUFFIX = ("\n\nBe accurate about what is CURRENT: notes can be replaced by later ones. "
          "When done, put your final answer on the last line, starting with 'ANSWER:'.\n\nQuestion: ")


def load_key():
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("Set OPENAI_API_KEY in the environment or in .env (gitignored).")


def done_trials():
    rows = []
    if RESULTS.exists():
        rows = [json.loads(l) for l in RESULTS.read_text().splitlines() if l.strip()]
    return rows


def spent(rows=None):
    """Total spend across EVERY results file, so pilots and smoke tests count toward the cap."""
    total = 0.0
    for f in (ROOT / "results").glob("*.jsonl"):
        for line in f.read_text().splitlines():
            if line.strip():
                total += json.loads(line).get("cost_usd") or 0
    return total


BUILTIN = ["bash", "read", "grep", "glob", "list", "write", "edit", "patch", "webfetch", "websearch",
           "todowrite", "todoread", "task", "skill", "question"]


def config(arm, model, write=False):
    """A dedicated `bench` agent with an explicit tool allowlist per arm.

    Markdown arm: read-only file tools + bash (like their grep/head/cat agents); with
    write=True (the write benchmark) it may also create and edit files.
    Native arm: only Native's MCP tools; every built-in is off and denied, so the agent
    cannot read the SQLite file directly (matches their "SQLite via MCP" setup).
    """
    md = {"bash", "read", "grep", "glob", "list"} | ({"write", "edit", "patch"} if write else set())
    allowed = {"markdown": md}.get(arm, set())
    tools = {t: (t in allowed) for t in BUILTIN}
    perm = {t: ("allow" if t in allowed else "deny") for t in BUILTIN if t not in ("patch",)}
    perm["external_directory"] = "deny"
    if arm.startswith("native"):
        tools["native_*"] = True
    cfg = {
        "$schema": "https://opencode.ai/config.json",
        "model": f"openai/{model}",
        "autoupdate": False,
        "share": "disabled",
        "tools": tools,
        "permission": perm,
        "agent": {"bench": {"mode": "primary", "model": f"openai/{model}", "tools": tools,
                            "permission": perm,
                            "prompt": ("You keep a company's shared notes up to date using only the tools you have."
                                       if write else
                                       "You answer questions about a company's notes using only the tools you have. "
                                       "You cannot edit anything.")}},
    }
    if arm.startswith("native"):
        cfg["mcp"] = {"native": {"type": "local", "enabled": True,
                                 "command": [str(NATIVE_BIN), "__DB__"]}}
    return cfg


def price(model, tokens):
    p = PRICES.get(model)
    if not p:
        return None
    uncached = max(tokens["input"] - tokens["cache_read"], 0)
    return (uncached * p["input"] + tokens["cache_read"] * p.get("cached_input", p["input"])
            + tokens["cache_write"] * p.get("cache_write", 0)
            + (tokens["output"] + tokens["reasoning"]) * p["output"]) / 1e6


def make_workspace(base, cfg, key):
    """Fresh trial dir: ws/ (agent's cwd, holds opencode.json) and isolated xdg/ dirs."""
    if base.exists():
        shutil.rmtree(base)
    ws, xdg = base / "ws", base / "xdg"
    for d in ("config", "data", "state", "cache"):
        (xdg / d).mkdir(parents=True)
    ws.mkdir(parents=True)
    (ws / "opencode.json").write_text(json.dumps(cfg, indent=2))
    env = {k: v for k, v in os.environ.items() if not k.startswith(("OPENCODE", "XDG_"))}
    # PWD must match cwd: OpenCode resolves the project directory from $PWD, and an
    # inherited PWD pointed agents at this repo (and its data/vault) instead of ws/.
    env.update(PWD=str(ws), OPENAI_API_KEY=key, XDG_CONFIG_HOME=str(xdg / "config"), XDG_DATA_HOME=str(xdg / "data"),
               XDG_STATE_HOME=str(xdg / "state"), XDG_CACHE_HOME=str(xdg / "cache"),
               OPENCODE_DISABLE_AUTOUPDATE="1")
    return ws, env


def opencode_session(base, ws, env, model, msg, timeout, name=""):
    """Run one headless OpenCode session and read its tokens, steps and tool calls back."""
    # OpenCode's first start on a fresh data dir can fail with "Unexpected server error"
    # (database init). A no-model command initialises it first.
    subprocess.run(["opencode", "session", "list"], cwd=ws, env=env, capture_output=True, timeout=120)
    t0 = time.time()
    timed_out = False
    try:
        proc = subprocess.run(["opencode", "run", "--pure", "--format", "json", "--agent", "bench",
                               "-m", f"openai/{model}", msg],
                              cwd=ws, env=env, capture_output=True, text=True, timeout=timeout)
        out, err = proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        timed_out = True
        out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = (e.stderr or b"").decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
    wall = time.time() - t0
    (base / f"{name}events.jsonl").write_text(out)
    (base / f"{name}stderr.txt").write_text(err)

    session = None
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        session = session or ev.get("sessionID") or (ev.get("part") or {}).get("sessionID")
    tokens = {"input": 0, "output": 0, "reasoning": 0, "cache_read": 0, "cache_write": 0}
    steps, tool_calls, tool_errors, text, oc_cost = 0, [], 0, "", 0.0
    if session:
        # Write straight to a file: piping `opencode export` truncates at 64 KiB.
        with open(base / f"{name}export.json", "w") as fh:
            subprocess.run(["opencode", "export", session], cwd=ws, env=env, stdout=fh,
                           stderr=subprocess.DEVNULL)
        raw = (base / f"{name}export.json").read_text()
        try:
            data = json.loads(raw[raw.index("{"):])
        except (ValueError, json.JSONDecodeError):
            data = {"messages": []}
        for m in data.get("messages", []):
            info = m.get("info", {})
            if info.get("role") != "assistant":
                continue
            t = info.get("tokens") or {}
            tokens["input"] += t.get("input", 0) + (t.get("cache") or {}).get("read", 0)
            tokens["cache_read"] += (t.get("cache") or {}).get("read", 0)
            tokens["cache_write"] += (t.get("cache") or {}).get("write", 0)
            tokens["output"] += t.get("output", 0)
            tokens["reasoning"] += t.get("reasoning", 0)
            oc_cost += info.get("cost") or 0
            for p in m.get("parts", []):
                if p.get("type") == "step-start":
                    steps += 1
                elif p.get("type") == "tool":
                    tool_calls.append(p.get("tool"))
                    st = p.get("state") or {}
                    # MCP tools report failures inside a completed call as {"error": ...}.
                    if st.get("status") == "error" or str(st.get("output", "")).lstrip().startswith('{"error"'):
                        tool_errors += 1
                elif p.get("type") == "text":
                    text = p.get("text", "") or text
    # Budget safety: charge the higher of our price-table estimate and OpenCode's own figure.
    cost = max(price(model, tokens) or 0, oc_cost)
    return {"tokens": tokens, "steps": steps, "tool_calls": tool_calls, "tool_errors": tool_errors,
            "text": text, "session": session, "wall": wall, "timed_out": timed_out, "cost": cost,
            "oc_cost": oc_cost, "err": err}


def run_trial(model, arm, q, run, key, timeout, workroot):
    tid = f"{TAG}{model}__{arm}__{q['id']}__r{run}"
    base = workroot / tid
    cfg = config(arm, model)
    if arm != "markdown":
        db = base / "native.db"
        cfg["mcp"]["native"]["command"][1] = str(db)
    ws, env = make_workspace(base, cfg, key)
    if arm == "markdown":
        shutil.copytree(DATA / "vault", ws / "vault")
    else:
        shutil.copy(NATIVE_DB, db)
    msg = PROMPT[arm] + SUFFIX + q["question"]
    s = opencode_session(base, ws, env, model, msg, timeout)
    tokens, text = s["tokens"], s["text"]
    answer = ""
    for line in reversed(text.splitlines()):
        if "ANSWER:" in line:
            answer = line.split("ANSWER:", 1)[1].strip()
            break
    answer = answer or text.strip()[-400:]
    return {
        "trial": tid, "corpus": TAG.rstrip("_") or "base", "model": model, "arm": arm, "qid": q["id"], "qtype": q["type"], "run": run,
        "answer": answer, "expected": q["answer"], "correct": grade(answer, q["keys"]),
        "tokens_total": tokens["input"] + tokens["output"] + tokens["reasoning"], **{f"tok_{k}": v for k, v in tokens.items()},
        "steps": s["steps"], "tool_calls": len(s["tool_calls"]), "tools_used": sorted(set(filter(None, s["tool_calls"]))),
        "wall_s": round(s["wall"], 1), "timed_out": s["timed_out"], "cost_usd": round(s["cost"], 6),
        "opencode_cost_usd": round(s["oc_cost"], 6), "session": s["session"],
        "error": None if s["session"] else (s["err"].strip().splitlines() or ["no session"])[-1][:300],
    }


def grade(answer, keys):
    a = answer.lower()
    return any(all(k.lower() in a for k in alt) for alt in keys)


def main():
    global RESULTS, DATA, NATIVE_DB, TAG
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--arms", nargs="+", default=["markdown", "native"])
    ap.add_argument("--questions", nargs="+", default=["all"])
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--first-run", type=int, default=1, help="e.g. 2 to add only run 2")
    ap.add_argument("--budget", type=float, default=9.90)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--keep", action="store_true", help="keep per-trial workspaces")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--data", default=str(DATA), help="corpus dir with vault/, native.db, questions.json")
    ap.add_argument("--tag", default="", help="corpus label, prefixed to trial ids")
    ap.add_argument("--headroom", type=float, default=0.05, help="$ reserved per in-flight trial")
    ap.add_argument("--out", default=str(RESULTS), help="results JSONL (budget counts every file in results/)")
    a = ap.parse_args()
    RESULTS = Path(a.out).resolve()
    DATA = Path(a.data).resolve()
    NATIVE_DB = DATA / "native.db"
    TAG = f"{a.tag}__" if a.tag else ""
    key = load_key()
    qs = json.loads((DATA / "questions.json").read_text())
    if a.questions != ["all"]:
        qs = [q for q in qs if q["id"] in a.questions]
    rows = done_trials()
    have = {r["trial"] for r in rows if not r.get("error")}
    # Trial workspaces must live OUTSIDE any git repo: OpenCode treats the enclosing git
    # root as the project, which let agents reach data/vault from the Native arm.
    workroot = (Path(tempfile.gettempdir()) / "native-bench-runs").resolve()
    workroot.mkdir(exist_ok=True)
    assert subprocess.run(["git", "rev-parse"], cwd=workroot, capture_output=True).returncode != 0, \
        "trial root is inside a git repo"
    RESULTS.parent.mkdir(exist_ok=True)
    jobs = [(model, arm, q, run) for run in range(a.first_run, a.runs + 1) for q in qs
            for model in a.models for arm in a.arms
            if f"{TAG}{model}__{arm}__{q['id']}__r{run}" not in have]
    lock = threading.Lock()
    stop = threading.Event()

    def work(job):
        model, arm, q, run = job
        if stop.is_set():
            return
        with lock:
            total = spent()
            # Leave headroom for trials already in flight.
            if total >= a.budget - a.headroom * a.workers:
                stop.set()
                print(f"BUDGET STOP at ${total:.2f}", flush=True)
                return
        r = run_trial(model, arm, q, run, key, a.timeout, workroot)
        with lock:
            with RESULTS.open("a") as f:
                f.write(json.dumps(r) + "\n")
            print(f"{r['trial']:55s} {'OK ' if r['correct'] else 'BAD'} tok={r['tokens_total']:>9,} "
                  f"steps={r['steps']:>3} {r['wall_s']:>6}s ${r['cost_usd']:.4f} "
                  f"total=${spent():.2f} {r['error'] or ''}", flush=True)
        if not a.keep and not r.get("error"):
            shutil.rmtree(workroot / r["trial"] / "ws", ignore_errors=True)
        # Always drop the per-trial DB copy (14-66 MB each); it filled the disk once.
        for f in (workroot / r["trial"]).glob("native.db*"):
            f.unlink(missing_ok=True)

    print(f"{len(jobs)} trials queued, spent so far ${spent():.2f}", flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        list(pool.map(work, jobs))
    print(f"DONE. total spent ${spent():.2f}", flush=True)


if __name__ == "__main__":
    main()
