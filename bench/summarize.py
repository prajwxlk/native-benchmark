"""Summarise results/*.jsonl into results/summary.md (tables reproducible from raw rows).

  python3 -I bench/summarize.py results/full.jsonl [more.jsonl ...]

Metrics follow Native's benchmark where possible:
  - tokens per fully correct answer = all tokens spent / number of correct answers
  - failed trials = wrong or no answer (incl. timeouts)
  - median steps (model turns) and median wall time
  - cost per correct answer (USD, from token counts x list prices)
"""
import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(paths):
    rows = []
    for p in paths:
        for line in Path(p).read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                if not r.get("error"):
                    rows.append(r)
    return rows


def agg(rows):
    n = len(rows)
    ok = sum(r["correct"] for r in rows)
    tok = sum(r["tokens_total"] for r in rows)
    cost = sum(r["cost_usd"] for r in rows)
    return {
        "n": n, "correct": ok, "acc": ok / n if n else 0,
        "tok_per_correct": tok / ok if ok else float("inf"),
        "tok_median": st.median(r["tokens_total"] for r in rows) if rows else 0,
        "steps_median": st.median(r["steps"] for r in rows) if rows else 0,
        "wall_median": st.median(r["wall_s"] for r in rows) if rows else 0,
        "cost": cost, "cost_per_correct": cost / ok if ok else float("inf"),
        "timeouts": sum(r["timed_out"] for r in rows),
    }


def fmt_tok(x):
    return "∞ (none correct)" if x == float("inf") else f"{x/1000:,.0f}k"


def ratio(a, b):
    if a in (0, float("inf")) or b in (0, float("inf")):
        return "n/a"
    return f"{a/b:.1f}×"


def main(paths):
    rows = load(paths)
    models = sorted({r["model"] for r in rows}, key=lambda m: [r["model"] for r in rows].index(m))
    out = ["# Results", "", f"{len(rows)} trials from {', '.join(Path(p).name for p in paths)}.", ""]

    out += ["## Headline: Markdown vs Native, per model", "",
            "| Model | Arm | Correct | Tokens per correct answer | Median tokens / trial | Median steps | Median time | Cost per correct |",
            "|---|---|---|---|---|---|---|---|"]
    by = defaultdict(list)
    for r in rows:
        by[(r["model"], r["arm"])].append(r)
        by[(r["model"], r["arm"], r["qtype"])].append(r)
        by[("ALL", r["arm"])].append(r)
        by[("ALL", r["arm"], r["qtype"])].append(r)
    arms = [a for a in ("markdown", "native", "native_hinted") if any(r["arm"] == a for r in rows)]
    for m in models + ["ALL"]:
        for arm in arms:
            g = agg(by[(m, arm)])
            if not g["n"]:
                continue
            out.append(f"| {m} | {arm} | {g['correct']}/{g['n']} ({g['acc']:.0%}) | {fmt_tok(g['tok_per_correct'])} | "
                       f"{g['tok_median']/1000:,.0f}k | {g['steps_median']:.0f} | {g['wall_median']:.0f}s | "
                       f"${g['cost_per_correct']:.4f} |")
    out += ["", "## Token ratio (Markdown ÷ Native, tokens per correct answer)", "",
            "| Model | All questions | Freshness | Lookup | Multi-hop | Accuracy MD → Native |", "|---|---|---|---|---|---|"]
    for m in models + ["ALL"]:
        cells = []
        for qt in (None, "freshness", "lookup", "multi_hop"):
            k_md = (m, "markdown") if qt is None else (m, "markdown", qt)
            k_nv = (m, "native") if qt is None else (m, "native", qt)
            cells.append(ratio(agg(by[k_md])["tok_per_correct"], agg(by[k_nv])["tok_per_correct"]))
        a_md, a_nv = agg(by[(m, "markdown")]), agg(by[(m, "native")])
        out.append(f"| {m} | " + " | ".join(cells) + f" | {a_md['acc']:.0%} → {a_nv['acc']:.0%} |")

    out += ["", "## Accuracy by question type", "", "| Model | Arm | Freshness | Lookup | Multi-hop |", "|---|---|---|---|---|"]
    for m in models + ["ALL"]:
        for arm in arms:
            cells = []
            for qt in ("freshness", "lookup", "multi_hop"):
                g = agg(by[(m, arm, qt)])
                cells.append(f"{g['correct']}/{g['n']}" if g["n"] else "–")
            out.append(f"| {m} | {arm} | " + " | ".join(cells) + " |")

    spend = defaultdict(float)
    for r in rows:
        spend[r["model"]] += r["cost_usd"]
    out += ["", "## Spend", "", "| Model | USD |", "|---|---|"]
    out += [f"| {m} | ${spend[m]:.2f} |" for m in models] + [f"| **Total** | **${sum(spend.values()):.2f}** |"]

    tools = defaultdict(lambda: defaultdict(int))
    for r in rows:
        for t in r.get("tools_used", []):
            tools[r["arm"]][t] += 1
    out += ["", "## Tools used (trials that used each)", ""]
    for arm, d in tools.items():
        out.append(f"- **{arm}**: " + ", ".join(f"{t} ({n})" for t, n in sorted(d.items(), key=lambda x: -x[1])))

    wrong = [r for r in rows if not r["correct"]]
    out += ["", f"## Wrong answers ({len(wrong)})", "", "| Trial | Expected | Got |", "|---|---|---|"]
    for r in sorted(wrong, key=lambda r: (r["qid"], r["model"], r["arm"])):
        got = (r["answer"] or "(no answer)").replace("|", "/").replace("\n", " ")[:160]
        out.append(f"| {r['model']} · {r['arm']} · {r['qid']} | {r['expected']} | {got} |")

    text = "\n".join(out) + "\n"
    dest = ROOT / "results" / ("summary.md" if len(paths) != 1 else f"summary-{Path(paths[0]).stem}.md")
    dest.write_text(text)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1:] or [str(ROOT / "results/full.jsonl")])
