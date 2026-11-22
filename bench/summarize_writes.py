"""Summarise write-benchmark trials into results/summary-writes.md.

  python3 -I bench/summarize_writes.py results/writes.jsonl [more.jsonl ...]
"""
import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS = ["markdown", "native", "native_hinted", "native_combined"]
# The typed status Native's own views use; fm.status facets copied from the import also pass the checks.
LIFE = [("T1", {"completed"}), ("T2", {"closed"})]


def k(n):
    return f"{n / 1000:.0f}k" if n >= 1000 else str(n)


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.0f}%)" if b else "–"


def main():
    files = [Path(f) for f in sys.argv[1:]] or [ROOT / "results/writes.jsonl"]
    rows = [json.loads(l) for f in files for l in f.read_text().splitlines() if l.strip()]
    rows = [r for r in rows if not r.get("error")]
    groups = defaultdict(list)
    for r in rows:
        groups[(r["model"], r["arm"])].append(r)
        groups[("ALL", r["arm"])].append(r)
    models = sorted({r["model"] for r in rows}) + ["ALL"]
    out = [f"# Write benchmark results\n\n{len(rows)} trials from {', '.join(f.name for f in files)}. "
           f"Reader model: {', '.join(sorted({r['reader_model'] for r in rows}))}.\n",
           "Each trial: one agent files a week of messages into the workspace (5 decisions replaced, 2 task "
           "status changes, 1 new task, 2 distractors), then a fresh reader answers 9 questions against the result.\n",
           "## Headline\n",
           "| Model | Setup | Runs | Changes applied | Replacements recorded | Distractors kept out | "
           "Next agent correct | Tokens / trial (median) | Tokens per correct change | Failed tool calls (median) | "
           "Time (median) | Cost / trial |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in models:
        for arm in ARMS:
            g = groups.get((m, arm))
            if not g:
                continue
            n = len(g)
            ch, cht = sum(r["changes_ok"] for r in g), sum(r["changes_total"] for r in g)
            toks = sum(r["tokens_total"] for r in g)
            out.append(
                f"| {m} | {arm} | {n} | {pct(ch, cht)} | {pct(sum(r['replacements_ok'] for r in g), 5 * n)} | "
                f"{pct(sum(r['distractors_ok'] for r in g), 2 * n)} | "
                f"{pct(sum(r['readback_ok'] for r in g), sum(r['readback_total'] for r in g))} | "
                f"{k(int(st.median(r['tokens_total'] for r in g)))} | {k(toks // ch) if ch else '–'} | "
                f"{st.median(r['tool_errors'] for r in g):.0f} | {st.median(r['wall_s'] for r in g):.0f}s | "
                f"${sum(r['cost_usd'] for r in g) / n:.3f} |")
    out += ["\n**Replacements recorded**: Native needs a typed `supersedes` link (or relationship) from the new "
            "record to the old decision; Markdown accepts any explicit marker a reader could use (the new note "
            "naming the old one with replace/supersede wording, or the old note edited to say it is superseded). "
            "The Markdown check is the more lenient one. **Next agent correct** is the setup-neutral test: a "
            "fresh reader answering questions about the new state.\n",
            "## Per check (pass rate across runs)\n"]
    checks = sorted({c for r in rows for c in r["checks"]})
    hdr = [(m, a) for m in models if m != "ALL" for a in ARMS if (m, a) in groups]
    out.append("| Check | " + " | ".join(f"{m} {a}" for m, a in hdr) + " |")
    out.append("|---|" + "---|" * len(hdr))
    for c in checks:
        cells = []
        for key in hdr:
            g = groups[key]
            cells.append(f"{sum(r['checks'][c] for r in g)}/{len(g)}")
        out.append(f"| {c} | " + " | ".join(cells) + " |")
    out.append("\n## How Native agents recorded replacements\n")
    out.append("| Model | Setup | Typed links | Prose only (no link) | Reversed link | New decision typed as Resolution "
               "| Task status in `lifecycle` field | Records without a name |")
    out.append("|---|---|---|---|---|---|---|---|")
    for m, a in hdr:
        if a == "markdown":
            continue
        g = groups[(m, a)]
        ds = [r["details"][rid] for r in g for rid in ("R1", "R2", "R3", "R4", "R5")]
        out.append(f"| {m} | {a} | {sum(r['replacements_ok'] for r in g)}/{5 * len(g)} | "
                   f"{sum(bool(d.get('prose_only')) for d in ds)} | {sum(bool(d.get('reversed')) for d in ds)} | "
                   f"{sum(bool(d.get('typed_as_decision')) for d in ds)}/{len(ds)} | "
                   f"{sum(r['details'][t].get('lifecycle') in ok for r in g for t, ok in LIFE)}/{2 * len(g)} | "
                   f"{sum(r.get('unnamed_records', 0) for r in g)} |")
    out.append("\n## Read-back, per question\n")
    qs = sorted({q for r in rows for q in r["readback"]}, key=lambda q: int(q[1:]))
    out.append("| Question | " + " | ".join(f"{m} {a}" for m, a in hdr) + " |")
    out.append("|---|" + "---|" * len(hdr))
    for q in qs:
        out.append(f"| {q} | " + " | ".join(f"{sum(r['readback'][q] for r in groups[key])}/{len(groups[key])}"
                                            for key in hdr) + " |")
    dest = ROOT / "results" / ("summary-writes.md" if files[0].name == "writes.jsonl" else f"summary-{files[0].stem}.md")
    dest.write_text("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    main()
