"""Write benchmark: can an agent keep the workspace current, and does the next agent then get it right?

Each trial:
  1. Writer: an agent gets data/writes/feed.md (a week of messages) and must update the
     workspace (Markdown vault, or a Native database through MCP).
  2. Grade the final state against data/writes/scenarios.json (deterministic; see grade()).
  3. Read-back: a fresh reader agent (fixed model) answers data/writes/readback.json against
     the updated workspace. Markdown is read by the Markdown reader; both Native arms are read
     by the hinted Native reader, so read-back differences come from what was written.

  python3 -I bench/gen_writes.py
  python3 -I bench/run_writes.py --models gpt-5-mini --arms markdown native native_hinted --runs 1 --budget 12

Results append to results/writes.jsonl (counted by the shared budget guard); what each agent
wrote is saved under results/writes/<trial>/ (changes.diff or events.json, plus state.json).
"""
import argparse
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run as R  # noqa: E402

ROOT = R.ROOT
DATA = ROOT / "data"
WD = DATA / "writes"
VAULT = DATA / "vault"
BASE_DB = DATA / "native.db"
OUT = ROOT / "results" / "writes.jsonl"
ART = ROOT / "results" / "writes"

TASK = ("You maintain the shared workspace of Fernwork, a startup. Below are new messages and meeting notes "
        "from the week of 13 October 2026. Update the workspace so it reflects them: record new decisions, "
        "update the status of tasks, and add new tasks. Only record what was actually agreed or done. "
        "When a new decision replaces an earlier one, record that it replaces it, so later readers know which "
        "one is current. Do not delete anything. When you are finished, reply with a short summary of what "
        "you changed.\n\n")
WHERE = {
    "markdown": "The workspace is a folder of Markdown notes (YAML frontmatter, [[wikilinks]]) in ./vault in your "
                "working directory. Follow the conventions the existing notes use.",
    "native": "The workspace is a Native workspace, available to you through the `native` MCP tools.",
}
# Same idea as the read benchmark's hint: emulate product-side docs, not extra capability.
WHERE["native_hinted"] = WHERE["native"] + (
    " Tips: you do not need to call bootstrap. Find records with records_read operation 'search' and arguments "
    "{query} only. " + R.WRITE_TIPS)
# The read hint and the write hint together (bench/run.py HINT_COMBINED).
WHERE["native_combined"] = WHERE["native"] + " " + R.HINT_COMBINED
# Every Native setup is read back by the same read-hint reader, so read-back compares what was written.
READER_ARM = {"markdown": "markdown", "native": "native_hinted", "native_hinted": "native_hinted",
              "native_combined": "native_hinted"}
REPLACE_WORDS = r"replac|supersed|instead of|no longer|switch(ed|ing)? from|mov(e|ed|ing) (away )?from|in place of"


def has_keys(text, keys):
    t = (text or "").lower()
    return any(all(k.lower() in t for k in alt) for alt in keys)


# ---------- state extraction: both arms reduce to the same shape ----------

def parse_md(text):
    fm, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            for line in text[3:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip().lower()] = v.strip().strip('"').strip("'")
            body = text[end + 4:]
    status_line = re.search(r"^Status:\s*(.+)$", body, re.M)
    return fm, (status_line.group(1).strip() if status_line else None)


def md_item(rel, text):
    fm, body_status = parse_md(text)
    name = fm.get("title") or Path(rel).stem
    statuses = [s.lower() for s in (fm.get("status"), body_status) if s]
    return {"id": rel, "name": name, "text": name + "\n" + text, "statuses": statuses,
            "decision": name.lower().startswith("decision") or fm.get("status", "").lower() in ("decided", "agreed", "accepted"),
            "task": name.lower().startswith("task") or rel.startswith("Fernwork HQ/Work/Tasks/")}


def markdown_state(vault_after, sc):
    before = {str(p.relative_to(VAULT)): p.read_text() for p in VAULT.rglob("*.md")}
    after = {str(p.relative_to(vault_after)): p.read_text(errors="replace") for p in vault_after.rglob("*.md")}
    title_to_rel = {md_item(r, t)["name"]: r for r, t in before.items()}
    new = [md_item(r, t) for r, t in after.items() if r not in before]
    modified = {r for r in before if r in after and after[r] != before[r]}

    def old(title):
        rel = title_to_rel[title]
        if rel not in after:
            return {"id": rel, "exists": False, "statuses": [], "text": "", "added": ""}
        it = md_item(rel, after[rel])
        added = "\n".join(l for l in after[rel].splitlines() if l not in set(before[rel].splitlines()))
        return {**it, "exists": True, "added": added, "modified": rel in modified}

    olds = {t: old(t) for t in scenario_titles(sc)}
    diff = subprocess.run(["diff", "-ruN", str(VAULT), str(vault_after)], capture_output=True, text=True).stdout
    diff = diff.replace(str(VAULT), "before").replace(str(vault_after), "after")
    return {"arm": "markdown", "new": new, "old": olds, "supersedes": None,
            "deleted": sorted(r for r in before if r not in after), "touched": sorted(modified)}, diff


def native_state(db, sc):
    c = sqlite3.connect(str(db))
    c.row_factory = sqlite3.Row
    c.execute("ATTACH DATABASE ? AS base", (str(BASE_DB),))
    q = lambda s, *a: [dict(r) for r in c.execute(s, a)]  # noqa: E731
    base_max = c.execute("SELECT max(seq) FROM base.content_events").fetchone()[0]
    def facets(rid):
        return {f["key"]: str(f["value"]).strip('"') for f in q("SELECT key, value FROM facet_values WHERE record_id = ?", rid)}

    def statuses(r, fv):
        # lifecycle is Native's typed status; imported notes also carry their frontmatter as fm.* facets,
        # and agents that copy the import's shape write fm.status instead. Both are structured fields.
        return [str(v).lower() for v in (r["lifecycle"], r["maturity"], *(fv[k] for k in fv if k.endswith("status"))) if v]

    new = []
    for r in q("SELECT id, type, kind, name, body, lifecycle, maturity FROM records "
               "WHERE id NOT IN (SELECT id FROM base.records)"):
        fv = facets(r["id"])
        name = r["name"] or fv.get("fm.title") or ""
        new.append({"id": r["id"], "name": name, "text": name + "\n" + (r["body"] or ""),
                    "nameless": not r["name"], "statuses": statuses(r, fv),
                    "type": r["type"], "kind": r["kind"],
                    "decision": (r["type"] == "Resolution" and (r["kind"] or "") not in ("proposal", "idea", "option"))
                    or name.lower().startswith("decision"),
                    "task": r["type"] == "WorkItem" or name.lower().startswith("task")})
    links = q("SELECT source_id, target_id, relationship, note FROM links WHERE id NOT IN (SELECT id FROM base.links)")
    # Governed relationships are a second way to say "supersedes"; count them too.
    rels = q("SELECT r.relationship_id, r.relationship_type, e.role, e.record_id FROM relationships r "
             "JOIN relationship_endpoints e USING (relationship_origin_db_id, relationship_id) "
             "WHERE r.relationship_id NOT IN (SELECT relationship_id FROM base.relationships)")
    sup = [(l["source_id"], l["target_id"]) for l in links if "supersed" in (l["relationship"] or "").lower()]
    by_rel = {}
    for r in rels:
        if "supersed" in (r["relationship_type"] or "").lower():
            by_rel.setdefault(r["relationship_id"], {})[r["role"]] = r["record_id"]
    sup += [(e.get("source") or e.get("subject"), e.get("target") or e.get("object")) for e in by_rel.values()]

    def old(title):
        rows = q("SELECT id, type, kind, name, body, lifecycle, maturity, deleted_at FROM records WHERE name = ?", title)
        if not rows:
            return {"id": None, "exists": False, "statuses": [], "text": "", "added": ""}
        r = rows[0]
        fv = facets(r["id"])
        touched = q("SELECT DISTINCT type FROM content_events WHERE seq > ? AND record_id = ?", base_max, r["id"])
        return {"id": r["id"], "exists": r["deleted_at"] is None, "name": r["name"],
                "text": (r["name"] or "") + "\n" + (r["body"] or ""), "added": "",
                "statuses": statuses(r, fv), "lifecycle": r["lifecycle"],
                "modified": bool(touched), "events": [t["type"] for t in touched]}

    olds = {t: old(t) for t in scenario_titles(sc)}
    events = q("SELECT seq, type, record_id, intent, created_at, payload FROM content_events WHERE seq > ? ORDER BY seq",
               base_max)
    for e in events:
        try:
            e["payload"] = json.loads(e["payload"])
        except (TypeError, ValueError):
            pass
    touched = q("SELECT DISTINCT r.name FROM content_events e JOIN base.records r ON r.id = e.record_id "
                "WHERE e.seq > ?", base_max)
    deleted = q("SELECT name FROM records WHERE deleted_at IS NOT NULL AND id IN "
                "(SELECT id FROM base.records WHERE deleted_at IS NULL)")
    c.close()
    return {"arm": "native", "new": new, "old": olds, "supersedes": sup, "links": links,
            "deleted": [d["name"] for d in deleted], "touched": sorted(t["name"] for t in touched),
            "intents": sorted({e["intent"] for e in events if e.get("intent")}),
            "event_types": [e["type"] for e in events]}, events


def scenario_titles(sc):
    return ([r["old"] for r in sc["replace"]] + [t["title"] for t in sc["tasks"]]
            + [d["current"] for d in sc["distractors"]])


# ---------- grading ----------

def grade(state, sc):
    """Deterministic checks on the final state. Returns {check_id: bool} plus details.

    Replacement recorded: Native needs a typed `supersedes` link or relationship from a new record
    holding the new value to the old decision (prose alone is not machine-readable, so it is
    reported separately as prose_only). Markdown accepts any explicit marker a reader could
    use: the new note naming the old one with replace/supersede wording, or the old note edited
    to say it is superseded/replaced/outdated.
    """
    checks, details = {}, {}
    new = state["new"]
    n_keys = lambda it: sum(has_keys(it["text"], r["keys"]) for r in sc["replace"])  # noqa: E731
    for r in sc["replace"]:
        old = state["old"][r["old"]]
        holders = [n for n in new if has_keys(n["text"], r["keys"])]
        cands = [n for n in holders if not n["task"] and (n["decision"] or has_keys(n["name"], r["keys"]))
                 and n_keys(n) < 3]
        checks[f"{r['id']}_new_decision"] = bool(cands)
        d = {"candidates": [n["name"] for n in cands], "typed_as_decision": any(n["decision"] for n in cands),
             "edited_old_in_place": bool(old.get("modified")) and has_keys(old.get("text", ""), r["keys"])}
        if state["supersedes"] is not None:
            ids = {n["id"] for n in holders}
            pairs = state["supersedes"]
            ok = any(s in ids and t == old["id"] for s, t in pairs)
            d["reversed"] = any(s == old["id"] and t in ids for s, t in pairs)
            d["prose_only"] = (not ok) and any(re.search(REPLACE_WORDS, n["text"], re.I) for n in cands)
        else:
            old_name = r["old"].lower()
            ok = any((old_name in n["text"].lower() or r["old_value"].lower() in n["text"].lower())
                     and re.search(REPLACE_WORDS, n["text"], re.I) for n in cands)
            ok = ok or bool(re.search(sc["stale_markers"], old.get("added", ""), re.I))
        checks[f"{r['id']}_replacement_recorded"] = bool(ok)
        details[r["id"]] = d
    for t in sc["tasks"]:
        st = state["old"][t["title"]]["statuses"]
        checks[f"{t['id']}_status"] = any(s.replace(" ", "_") in t["accept"] or s in t["accept"] for s in st)
        details[t["id"]] = {"statuses": st, "lifecycle": state["old"][t["title"]].get("lifecycle")}
    for t in sc["new_tasks"]:
        cands = [n for n in new if has_keys(n["name"], t["name_keys"])]
        checks[f"{t['id']}_new_task"] = any(t["owner"].lower() in n["text"].lower() for n in cands)
        details[t["id"]] = {"candidates": [n["name"] for n in cands]}
    for dd in sc["distractors"]:
        bad = [n["name"] for n in new if n["decision"] and has_keys(n["name"], dd["forbid_keys"])]
        cur = state["old"][dd["current"]]
        if state["supersedes"] is not None:
            superseded = any(t == cur["id"] for _, t in state["supersedes"])
        else:
            superseded = bool(re.search(sc["stale_markers"], cur.get("added", ""), re.I))
        checks[f"{dd['id']}_not_recorded"] = not bad and not superseded
        details[dd["id"]] = {"wrong_decisions": bad, "current_marked_superseded": superseded}
    checks["no_deletions"] = not state["deleted"]
    return checks, details


def summarize_checks(checks):
    positive = [k for k in checks if k[0] in "RT"]
    return {"changes_ok": sum(checks[k] for k in positive), "changes_total": len(positive),
            "replacements_ok": sum(v for k, v in checks.items() if k.endswith("_replacement_recorded")),
            "new_decisions_ok": sum(v for k, v in checks.items() if k.endswith("_new_decision")),
            "tasks_ok": sum(v for k, v in checks.items() if k[0] == "T"),
            "distractors_ok": sum(v for k, v in checks.items() if k[0] == "D"),
            "no_deletions": checks["no_deletions"]}


# ---------- read-back ----------

def readback(arm, base, ws_writer, db, key, model, timeout):
    qs = json.loads((WD / "readback.json").read_text())
    rarm = READER_ARM[arm]
    rbase = base / "reader"
    cfg = R.config(rarm, model)
    if rarm != "markdown":
        cfg["mcp"]["native"]["command"][1] = str(db)
    ws, env = R.make_workspace(rbase, cfg, key)
    if rarm == "markdown":
        shutil.copytree(ws_writer / "vault", ws / "vault")
    msg = (R.PROMPT[rarm] + "\n\nBe accurate about what is CURRENT: notes can be replaced by later ones. "
           "Answer every question below. When done, give each final answer on its own line as "
           "'A1: ...', 'A2: ...' and so on.\n\n" + "\n".join(f"Q{i + 1}. {q['question']}" for i, q in enumerate(qs)))
    s = R.opencode_session(rbase, ws, env, model, msg, timeout)
    answers = {}
    for line in s["text"].splitlines():
        m = re.match(r"\W*A(\d+)\s*[:.)-]\s*(.*)", line.strip())
        if m:
            answers[int(m.group(1))] = m.group(2).strip()
    graded = {q["id"]: {"answer": answers.get(i + 1, ""), "correct": R.grade(answers.get(i + 1, ""), q["keys"])}
              for i, q in enumerate(qs)}
    return graded, s


# ---------- one trial ----------

def run_one(model, arm, run, key, a, workroot):
    sc = json.loads((WD / "scenarios.json").read_text())
    tid = f"writes__{model}__{arm}__r{run}"
    base = workroot / tid
    cfg = R.config(arm, model, write=True)
    db = base / "native.db"
    if arm != "markdown":
        cfg["mcp"]["native"]["command"][1] = str(db)
    ws, env = R.make_workspace(base, cfg, key)
    if arm == "markdown":
        shutil.copytree(VAULT, ws / "vault")
    else:
        shutil.copy(BASE_DB, db)
    msg = TASK + WHERE[arm] + "\n\n" + (WD / "feed.md").read_text()
    s = R.opencode_session(base, ws, env, model, msg, a.timeout)
    art = ART / tid
    if art.exists():
        shutil.rmtree(art)
    art.mkdir(parents=True)
    if arm == "markdown":
        state, diff = markdown_state(ws / "vault", sc)
        (art / "changes.diff").write_text(diff)
    else:
        state, events = native_state(db, sc)
        (art / "events.json").write_text(json.dumps(events, indent=1, ensure_ascii=False))
    checks, details = grade(state, sc)
    (art / "state.json").write_text(json.dumps({"checks": checks, "details": details, **state}, indent=1,
                                               ensure_ascii=False, default=str))
    (art / "writer_reply.md").write_text(s["text"])
    rb, rs = readback(arm, base, ws, db, key, a.reader_model, a.reader_timeout)
    (art / "readback.json").write_text(json.dumps(rb, indent=1, ensure_ascii=False))
    (art / "reader_reply.md").write_text(rs["text"])
    t = s["tokens"]
    row = {
        "trial": tid, "model": model, "arm": arm, "run": run, "reader_model": a.reader_model,
        **summarize_checks(checks), "checks": checks, "details": details,
        "readback_ok": sum(v["correct"] for v in rb.values()), "readback_total": len(rb),
        "readback": {k: v["correct"] for k, v in rb.items()},
        "tokens_total": t["input"] + t["output"] + t["reasoning"], **{f"tok_{k}": v for k, v in t.items()},
        "steps": s["steps"], "tool_calls": len(s["tool_calls"]), "tool_errors": s["tool_errors"],
        "tools_used": sorted(set(filter(None, s["tool_calls"]))),
        "wall_s": round(s["wall"], 1), "timed_out": s["timed_out"],
        "writer_cost_usd": round(s["cost"], 6), "reader_cost_usd": round(rs["cost"], 6),
        "cost_usd": round(s["cost"] + rs["cost"], 6),
        "reader_tokens": rs["tokens"]["input"] + rs["tokens"]["output"] + rs["tokens"]["reasoning"],
        "reader_timed_out": rs["timed_out"], "session": s["session"],
        "new_records": len(state["new"]), "touched_existing": len(state["touched"]),
        "unnamed_records": sum(bool(n.get("nameless")) for n in state["new"]),
        "error": None if s["session"] else (s["err"].strip().splitlines() or ["no session"])[-1][:300],
    }
    if not a.keep:
        shutil.rmtree(base, ignore_errors=True)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--arms", nargs="+", default=["markdown", "native", "native_hinted"])
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--first-run", type=int, default=1)
    ap.add_argument("--reader-model", default="gpt-5-mini")
    ap.add_argument("--budget", type=float, required=True, help="total $ across every results/*.jsonl")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--reader-timeout", type=int, default=400)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--headroom", type=float, default=0.30, help="$ reserved per in-flight trial")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    out = Path(a.out).resolve()
    key = R.load_key()
    have = set()
    if out.exists():
        have = {json.loads(l)["trial"] for l in out.read_text().splitlines()
                if l.strip() and not json.loads(l).get("error")}
    workroot = (Path(tempfile.gettempdir()) / "native-bench-runs").resolve()
    workroot.mkdir(exist_ok=True)
    assert subprocess.run(["git", "rev-parse"], cwd=workroot, capture_output=True).returncode != 0, \
        "trial root is inside a git repo"
    jobs = [(m, arm, r) for r in range(a.first_run, a.runs + 1) for m in a.models for arm in a.arms
            if f"writes__{m}__{arm}__r{r}" not in have]
    lock, stop = threading.Lock(), threading.Event()

    def work(job):
        if stop.is_set():
            return
        with lock:
            total = R.spent()
            if total >= a.budget - a.headroom * a.workers:
                stop.set()
                print(f"BUDGET STOP at ${total:.2f}", flush=True)
                return
        row = run_one(*job, key, a, workroot)
        with lock:
            with out.open("a") as f:
                f.write(json.dumps(row) + "\n")
            print(f"{row['trial']:45s} changes {row['changes_ok']}/{row['changes_total']} "
                  f"repl {row['replacements_ok']}/5 distr {row['distractors_ok']}/2 "
                  f"readback {row['readback_ok']}/{row['readback_total']} tok={row['tokens_total']:>9,} "
                  f"err={row['tool_errors']} {row['wall_s']}s ${row['cost_usd']:.3f} total=${R.spent():.2f} "
                  f"{row['error'] or ''}", flush=True)

    print(f"{len(jobs)} write trials queued, spent so far ${R.spent():.2f}", flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        list(pool.map(work, jobs))
    print(f"DONE. total spent ${R.spent():.2f}", flush=True)


if __name__ == "__main__":
    main()
