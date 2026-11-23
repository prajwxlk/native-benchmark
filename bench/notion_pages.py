"""Turn the Fernwork vault into Notion pages for the Notion AI test (findings/notion-ai.md).

  python3 -I bench/notion_pages.py "data/vault/Fernwork HQ" <out_dir>

Writes one JSON file per batch of up to 50 pages, grouped by top-level folder, each a list of
{"properties": {"title"}, "content"} ready for the Notion MCP create-pages tool. Frontmatter
becomes plain "key: value" lines and [[wikilinks]] become plain text.
"""
import json, re, sys
from pathlib import Path

VAULT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
SIZE = 50

def convert(text):
    title, meta, body = None, [], text
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        body = text[m.end():]
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            v = v.strip().strip('"')
            if k.strip() == "title":
                title = v
            else:
                meta.append(f"{k.strip()}: {v}")
    body = re.sub(r"\[\[([^\]|]+)(\|[^\]]+)?\]\]", r"\1", body)
    lines = meta + [""] + body.strip("\n").splitlines()
    out = []
    for i, line in enumerate(lines):
        out.append(line)
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        plain = lambda s: s.strip() and not re.match(r"\s*([-*+] |\d+\. |#)", s)
        if plain(line) and plain(nxt):
            out.append("")  # each plain line becomes its own paragraph
    return title, "\n".join(out).strip() + "\n"

total = 0
for folder in sorted(p for p in VAULT.iterdir() if p.is_dir()):
    pages = []
    for f in sorted(folder.rglob("*.md")):
        title, content = convert(f.read_text())
        pages.append({"properties": {"title": title or f.stem}, "content": content})
    for n in range(0, len(pages), SIZE):
        batch = pages[n:n + SIZE]
        (OUT / f"{folder.name}_{n // SIZE + 1}.json").write_text(json.dumps(batch, ensure_ascii=False, indent=1))
        total += len(batch)
print(total)
