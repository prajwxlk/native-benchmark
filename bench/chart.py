"""Draw the README charts (light + dark SVG) from the raw results.

  python3 -I bench/chart.py

Writes docs/chart-base-{light,dark}.svg and docs/chart-10x-{light,dark}.svg.
Numbers come from the same files and maths as the README tables.
"""
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

THEMES = {
    "light": {
        "surface": "#fcfcfb", "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
        "grid": "#e1e0d9", "axis": "#c3c2b7",
        "series": {"markdown": "#2a78d6", "native": "#eb6834", "native_hinted": "#1baf7a"},
    },
    "dark": {
        "surface": "#1a1a19", "ink": "#f0efec", "ink2": "#c3c2b7", "muted": "#898781",
        "grid": "#2c2c2a", "axis": "#383835",
        "series": {"markdown": "#3987e5", "native": "#d95926", "native_hinted": "#199e70"},
    },
}

FONT = 'system-ui, -apple-system, &quot;Segoe UI&quot;, sans-serif'


def stats(paths):
    by = defaultdict(list)
    for r in load([ROOT / p for p in paths]):
        by[(r["model"], r["arm"])].append(r)
        by[("ALL", r["arm"])].append(r)
    return {k: agg(v) for k, v in by.items()}


def bar(x0, y, w, h, r=4):
    """Bar anchored at x0, rounded only at its data end."""
    r = min(r, w, h / 2)
    return (f"M{x0},{y} H{x0 + w - r} Q{x0 + w},{y} {x0 + w},{y + r} "
            f"V{y + h - r} Q{x0 + w},{y + h} {x0 + w - r},{y + h} H{x0} Z")


def draw(theme, title, subtitle, groups, arms, xmax, note):
    t = THEMES[theme]
    W, left, right = 760, 150, 110
    plot_w = W - left - right
    bh, gap, group_gap = 14, 2, 18
    top = 108
    group_h = len(arms) * bh + (len(arms) - 1) * gap
    H = top + len(groups) * (group_h + group_gap) + 56
    sx = lambda v: left + plot_w * v / xmax  # noqa: E731

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="{FONT}" role="img" aria-label="{escape(title)}">',
         f'<rect width="{W}" height="{H}" rx="8" fill="{t["surface"]}"/>',
         f'<text x="24" y="34" font-size="17" font-weight="600" fill="{t["ink"]}">{escape(title)}</text>',
         f'<text x="24" y="56" font-size="13" fill="{t["ink2"]}">{escape(subtitle)}</text>']

    # Legend
    lx = 24
    for key, label in arms:
        o.append(f'<rect x="{lx}" y="72" width="12" height="12" rx="3" fill="{t["series"][key]}"/>')
        o.append(f'<text x="{lx + 18}" y="82.5" font-size="13" fill="{t["ink2"]}">{escape(label)}</text>')
        lx += 18 + 7 * len(label) + 24

    # Gridlines and axis labels
    plot_bottom = H - 56
    step = 20000
    for v in range(0, xmax + 1, step):
        x = sx(v)
        color = t["axis"] if v == 0 else t["grid"]
        o.append(f'<line x1="{x}" y1="{top - 8}" x2="{x}" y2="{plot_bottom}" stroke="{color}" stroke-width="1"/>')
        o.append(f'<text x="{x}" y="{plot_bottom + 18}" font-size="12" fill="{t["muted"]}" '
                 f'text-anchor="middle">{v // 1000}k</text>')

    y = top
    for gi, (label, tag, data) in enumerate(groups):
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
            v = g["tok_per_correct"]
            w = sx(v) - left
            desc = f'{label}, {arm_label}: {v / 1000:.0f}k tokens per correct answer, {g["acc"]:.0%} correct'
            o.append(f'<path d="{bar(left, by, w, bh)}" fill="{t["series"][key]}"><title>{escape(desc)}</title></path>')
            o.append(f'<text x="{left + w + 6}" y="{by + 11}" font-size="12" fill="{t["ink2"]}">'
                     f'<tspan font-weight="600" fill="{t["ink"]}">{v / 1000:.0f}k</tspan> · {g["acc"]:.0%} correct</text>')
        y += group_h + group_gap

    o.append(f'<text x="24" y="{H - 10}" font-size="11" fill="{t["muted"]}">{escape(note)}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


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

    for theme in THEMES:
        (OUT / f"chart-base-{theme}.svg").write_text(draw(
            theme, "Tokens per correct answer, base corpus (333 notes)",
            "Shorter bar = cheaper. Label shows tokens per correct answer and % of questions answered correctly.",
            groups, ARMS, 100000,
            "“All models” for Native + hint covers 4 models (gpt-5.4-mini not run). Source: results/*.jsonl"))
        (OUT / f"chart-10x-{theme}.svg").write_text(draw(
            theme, "Tokens per correct answer, 10× corpus (2,497 notes)",
            "Shorter bar = cheaper. Default Native only (no hint) at this size.",
            groups10, arms10, 100000, "Source: results/scale10.jsonl"))
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("chart-*.svg"))))


if __name__ == "__main__":
    main()
