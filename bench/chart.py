"""Draw the README charts (light + dark SVG) from the raw results.

  python3 -I bench/chart.py

Writes docs/chart-{base,10x,writes,combined,notion}-{light,dark}.svg.
Numbers come from the same files and maths as the README tables.
"""
import statistics
import sys
from collections import defaultdict
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from summarize import agg, load  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"

MODELS = [
    ("gpt-5-nano", "gpt-5-nano", "cheapest"),
    ("gpt-5-mini", "gpt-5-mini", ""),
    ("gpt-5.4-mini", "gpt-5.4-mini", ""),
    ("gpt-5.6-luna", "gpt-5.6-luna", ""),
    ("gpt-5.6-terra", "gpt-5.6-terra", "strongest"),
]
ARMS = [("markdown", "Markdown"), ("native", "Native (default)"), ("native_hinted", "Native + hint")]
HINT_ARMS = [("native_hinted", "Separate hint"), ("native_combined", "Combined hint")]
NOTION_ARMS = [("notion_ai", "Notion AI"), ("markdown", "Markdown"), ("native", "Native (default)"),
               ("native_hinted", "Native + hint")]
QTYPES = [("freshness", "Freshness", "10 questions"), ("lookup", "Lookup", "6 questions"),
          ("multi_hop", "Two-step", "4 questions")]
WRITE_MODELS = [m for m in MODELS if m[0] in ("gpt-5-nano", "gpt-5-mini", "gpt-5.6-luna")]

THEMES = {
    "light": {
        "surface": "#fcfcfb", "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
        "grid": "#e1e0d9", "axis": "#c3c2b7",
        "series": {"markdown": "#2a78d6", "native": "#eb6834", "native_hinted": "#1baf7a",
                   "native_combined": "#eda100", "notion_ai": "#7d6bd6"},
    },
    "dark": {
        "surface": "#1a1a19", "ink": "#f0efec", "ink2": "#c3c2b7", "muted": "#898781",
        "grid": "#2c2c2a", "axis": "#383835",
        "series": {"markdown": "#3987e5", "native": "#d95926", "native_hinted": "#199e70",
                   "native_combined": "#c98500", "notion_ai": "#9585e6"},
    },
}

FONT = 'system-ui, -apple-system, &quot;Segoe UI&quot;, sans-serif'


def stats(paths):
    """Read runs: tokens per correct answer, % of questions correct."""
    by = defaultdict(list)
    for r in load([ROOT / p for p in paths]):
        by[(r["model"], r["arm"])].append(r)
        by[("ALL", r["arm"])].append(r)
    return {k: {"n": g["n"], "acc": g["acc"], "v": g["tok_per_correct"]} for k, v in by.items() for g in [agg(v)]}


def write_stats(paths):
    """Write runs: tokens per correct change, % of changes applied (as in summarize_writes.py)."""
    by = defaultdict(list)
    for r in load([ROOT / p for p in paths]):
        by[(r["model"], r["arm"])].append(r)
        by[("ALL", r["arm"])].append(r)
    out = {}
    for k, g in by.items():
        ok, total = sum(r["changes_ok"] for r in g), sum(r["changes_total"] for r in g)
        out[k] = {"n": len(g), "acc": ok / total, "v": sum(r["tokens_total"] for r in g) / ok if ok else float("inf")}
    return out


def notion_stats(base_paths, notion_paths):
    """% correct by question type, and median seconds per answer, for Notion AI next to the base-corpus arms."""
    rows = load([ROOT / p for p in base_paths]) + load([ROOT / p for p in notion_paths])
    by = defaultdict(list)
    for r in rows:
        by[(r["qtype"], r["arm"])].append(r)
        by[("ALL", r["arm"])].append(r)
    out = {}
    for k, g in by.items():
        ok = sum(r["correct"] for r in g)
        out[k] = {"n": len(g), "ok": ok, "acc": ok / len(g), "v": 100 * ok / len(g),
                  "secs": statistics.median(r["wall_s"] for r in g)}
    return out


def bar(x0, y, w, h, r=4):
    """Bar anchored at x0, rounded only at its data end."""
    r = min(r, w, h / 2)
    return (f"M{x0},{y} H{x0 + w - r} Q{x0 + w},{y} {x0 + w},{y + r} "
            f"V{y + h - r} Q{x0 + w},{y + h} {x0 + w - r},{y + h} H{x0} Z")


def panel(heading, groups, xmax=100000, unit="correct answer", acc_word="correct", step=20000,
          tick=None, label=None):
    """tick(v) formats an axis value; label(g) -> (bold, rest, tooltip) overrides the bar label."""
    return {"heading": heading, "groups": groups, "xmax": xmax, "unit": unit, "acc_word": acc_word, "step": step,
            "tick": tick or (lambda v: f"{v // 1000}k"), "label": label}


def draw(theme, title, subtitle, arms, panels, note):
    """One or more stacked panels of grouped horizontal bars sharing a legend."""
    t = THEMES[theme]
    W, left, right = 760, 150, 110
    plot_w = W - left - right
    bh, gap, group_gap, panel_gap = 14, 2, 18, 20
    group_h = len(arms) * bh + (len(arms) - 1) * gap

    o = [f'<text x="24" y="34" font-size="17" font-weight="600" fill="{t["ink"]}">{escape(title)}</text>',
         f'<text x="24" y="56" font-size="13" fill="{t["ink2"]}">{escape(subtitle)}</text>']

    # Legend
    lx = 24
    for key, label in arms:
        o.append(f'<rect x="{lx}" y="72" width="12" height="12" rx="3" fill="{t["series"][key]}"/>')
        o.append(f'<text x="{lx + 18}" y="82.5" font-size="13" fill="{t["ink2"]}">{escape(label)}</text>')
        lx += 18 + 7 * len(label) + 24

    y = 108
    for pi, p in enumerate(panels):
        if pi:
            y += panel_gap
        if p["heading"]:
            o.append(f'<text x="24" y="{y + 4}" font-size="13" font-weight="600" fill="{t["ink"]}">'
                     f'{escape(p["heading"])}</text>')
            y += 26
        xmax = p["xmax"]
        sx = lambda v: left + plot_w * v / xmax  # noqa: E731
        top = y
        plot_bottom = top + len(p["groups"]) * (group_h + group_gap)

        # Gridlines and axis labels
        for v in range(0, xmax + 1, p["step"]):
            x = sx(v)
            color = t["axis"] if v == 0 else t["grid"]
            o.append(f'<line x1="{x}" y1="{top - 8}" x2="{x}" y2="{plot_bottom}" stroke="{color}" stroke-width="1"/>')
            o.append(f'<text x="{x}" y="{plot_bottom + 18}" font-size="12" fill="{t["muted"]}" '
                     f'text-anchor="middle">{p["tick"](v)}</text>')

        for gi, (label, tag, data) in enumerate(p["groups"]):
            if label == "All models" and gi:
                o.append(f'<line x1="24" y1="{y - group_gap / 2}" x2="{W - 24}" y2="{y - group_gap / 2}" '
                         f'stroke="{t["grid"]}" stroke-width="1"/>')
            cy = y + group_h / 2
            weight = "600" if label == "All models" else "400"
            o.append(f'<text x="{left - 12}" y="{cy + (0 if tag else 4.5)}" font-size="13" font-weight="{weight}" '
                     f'fill="{t["ink"]}" text-anchor="end">{escape(label)}</text>')
            if tag:
                o.append(f'<text x="{left - 12}" y="{cy + 15}" font-size="11" fill="{t["muted"]}" '
                         f'text-anchor="end">{escape(tag)}</text>')
            for ai, (key, arm_label) in enumerate(arms):
                by = y + ai * (bh + gap)
                g = data.get(key)
                if not g or not g["n"]:
                    o.append(f'<text x="{left + 6}" y="{by + 11}" font-size="12" fill="{t["muted"]}" '
                             f'font-style="italic">not run</text>')
                    continue
                v = g["v"]
                w = max(sx(v) - left, 0.5)
                if p["label"]:
                    bold, rest, desc = p["label"](g)
                    desc = f"{label}, {arm_label}: {desc}"
                else:
                    bold, rest = f"{v / 1000:.0f}k", f'{g["acc"]:.0%} {p["acc_word"]}'
                    desc = (f'{label}, {arm_label}: {v / 1000:.0f}k tokens per {p["unit"]}, '
                            f'{g["acc"]:.0%} {p["acc_word"]}')
                o.append(f'<path d="{bar(left, by, w, bh)}" fill="{t["series"][key]}">'
                         f'<title>{escape(desc)}</title></path>')
                o.append(f'<text x="{left + w + 6}" y="{by + 11}" font-size="12" fill="{t["ink2"]}">'
                         f'<tspan font-weight="600" fill="{t["ink"]}">{escape(bold)}</tspan>'
                         f'{" · " + escape(rest) if rest else ""}</text>')
            y += group_h + group_gap
        y = plot_bottom + 26

    H = y + 30
    o.append(f'<text x="24" y="{H - 10}" font-size="11" fill="{t["muted"]}">{escape(note)}</text>')
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'font-family="{FONT}" role="img" aria-label="{escape(title)}">',
            f'<rect width="{W}" height="{H}" rx="8" fill="{t["surface"]}"/>']
    return "\n".join(head + o + ["</svg>"]) + "\n"


def main():
    OUT.mkdir(exist_ok=True)
    # Base corpus: same files as the README tables (recheck.jsonl is a consistency check, not counted).
    base = stats(["results/pilot.jsonl", "results/full.jsonl", "results/repeat.jsonl", "results/hinted.jsonl"])
    groups = [(name, tag, {a: base.get((m, a)) for a, _ in ARMS}) for m, name, tag in MODELS]
    groups.append(("All models", "", {a: base.get(("ALL", a)) for a, _ in ARMS}))

    big = stats(["results/scale10.jsonl"])
    arms10 = ARMS[:2]
    models10 = [(m, n, t) for m, n, t in MODELS if (m, "markdown") in big]
    groups10 = [(name, tag, {a: big.get((m, a)) for a, _ in arms10}) for m, name, tag in models10]

    writes = write_stats(["results/writes.jsonl"])
    groups_w = [(name, tag, {a: writes.get((m, a)) for a, _ in ARMS}) for m, name, tag in WRITE_MODELS]
    groups_w.append(("All models", "", {a: writes.get(("ALL", a)) for a, _ in ARMS}))

    combined = stats(["results/combined-read.jsonl"])
    read_models = [(m, n, "") for m, n, _ in MODELS if (m, "native_combined") in combined]
    groups_cr = [(name, tag, {a: combined.get((m, a)) for a, _ in HINT_ARMS}) for m, name, tag in read_models]
    groups_cr.append(("All models", "", {a: combined.get(("ALL", a)) for a, _ in HINT_ARMS}))
    groups_cw = [(name, "", {a: writes.get((m, a)) for a, _ in HINT_ARMS}) for m, name, _ in WRITE_MODELS]
    groups_cw.append(("All models", "", {a: writes.get(("ALL", a)) for a, _ in HINT_ARMS}))

    for theme in THEMES:
        (OUT / f"chart-base-{theme}.svg").write_text(draw(
            theme, "Tokens per correct answer, base corpus (333 notes)",
            "Shorter bar = cheaper. Label shows tokens per correct answer and % of questions answered correctly.",
            ARMS, [panel(None, groups)],
            "“All models” for Native + hint covers 4 models (gpt-5.4-mini not run). Source: results/*.jsonl"))
        (OUT / f"chart-10x-{theme}.svg").write_text(draw(
            theme, "Tokens per correct answer, 10× corpus (2,497 notes)",
            "Shorter bar = cheaper. Default Native only (no hint) at this size.",
            arms10, [panel(None, groups10)], "Source: results/scale10.jsonl"))
        (OUT / f"chart-writes-{theme}.svg").write_text(draw(
            theme, "Tokens per correct change, write benchmark",
            "Shorter bar = cheaper. Label shows tokens per correct change and % of changes applied correctly.",
            ARMS, [panel(None, groups_w, 160000, "correct change", "applied")],
            "3 runs per model and setup; Native + hint is the write hint. Source: results/writes.jsonl"))
        (OUT / f"chart-combined-{theme}.svg").write_text(draw(
            theme, "One combined hint vs a hint per task",
            "Shorter bar = cheaper. Separate hint = the read hint for reading, the write hint for writing.",
            HINT_ARMS,
            [panel("Reading: tokens per correct answer", groups_cr, 80000),
             panel("Writing: tokens per correct change", groups_cw, 80000, "correct change", "applied")],
            "Reading: 1 run per question. Writing: 3 runs. Source: results/combined-read.jsonl, results/writes.jsonl"))
    notion_files = [ROOT / "results/notion-ai.jsonl"]
    if all(f.exists() for f in notion_files):
        ns = notion_stats(["results/pilot.jsonl", "results/full.jsonl", "results/repeat.jsonl",
                           "results/hinted.jsonl"], ["results/notion-ai.jsonl"])
        groups_acc = [(name, tag, {a: ns.get((q, a)) for a, _ in NOTION_ARMS}) for q, name, tag in QTYPES]
        groups_acc.append(("All models", "", {a: ns.get(("ALL", a)) for a, _ in NOTION_ARMS}))
        groups_acc[-1] = ("All 20", "", groups_acc[-1][2])
        time_groups = [("All 20", "", {a: dict(g, v=g["secs"]) if (g := ns.get(("ALL", a))) else None
                                       for a, _ in NOTION_ARMS})]
        pct = dict(xmax=100, step=20, tick=lambda v: f"{v}%",
                   label=lambda g: (f'{g["acc"]:.0%}', f'{g["ok"]}/{g["n"]}',
                                    f'{g["acc"]:.0%} correct ({g["ok"]}/{g["n"]})'))
        secs = dict(xmax=60, step=10, tick=lambda v: f"{v}s",
                    label=lambda g: (f'{g["v"]:.0f}s', "", f'median {g["v"]:.0f}s per answer'))
        for theme in THEMES:
            (OUT / f"chart-notion-{theme}.svg").write_text(draw(
                theme, "Notion AI vs Native on the same 20 questions",
                "Longer bar = more correct. Same synthetic workspace (333 notes); answers graded by the same script.",
                NOTION_ARMS,
                [panel("% of answers correct, by question type", groups_acc, **pct),
                 panel("Median seconds per answer (Notion AI's own timer; others include harness startup)", time_groups, **secs)],
                "Notion AI: 1 run per question, Auto model. Others: all 5 OpenAI models pooled. "
                "Source: results/notion-ai.jsonl, results/*.jsonl"))
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("chart-*.svg"))))


if __name__ == "__main__":
    main()
