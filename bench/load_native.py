"""Load the synthetic vault into a fresh Native database (the Native arm).

1. Write a native.enrichment.v1 sidecar from ground truth (record types, task lifecycle,
   task -implements-> decision). This stands in for `native enrich`, which would infer
   the same from text with an LLM; we use ground truth so the comparison isn't about
   enrichment quality.
2. `native import --enrichment` the same folder the Markdown arm reads.
3. Assert typed `supersedes` relationships (newer decision -> older decision) through
   Native's MCP tools, since import only lists supersession candidates.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp import Native  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--data=")), ROOT / "data")).resolve()
VAULT = (DATA / "vault").resolve()
DB = DATA / "native.db"
NATIVE = ROOT / "vendor/native/target/debug/native"


def title_of(text):
    for line in text.splitlines()[1:6]:
        if line.startswith("title: "):
            return json.loads(line[7:])
    return None


def main():
    links_only = "--links-only" in sys.argv
    if DB.exists() and not links_only:
        raise SystemExit(f"{DB} exists; move it aside first (or pass --links-only)")
    truth = json.loads((DATA / "truth.json").read_text())
    notes, by_title = {}, {}
    for f in sorted(VAULT.rglob("*.md")):
        rel = str(f.relative_to(VAULT))
        text = f.read_text()
        title = title_of(text)
        by_title[title] = rel
        if title in truth["decisions"]:
            t, k, life, dt = "Resolution", "decision", None, truth["decisions"][title]["date"]
        elif title in truth["tasks"]:
            t, k, life, dt = "WorkItem", "task", truth["tasks"][title]["status"], None
        elif title in truth["people"]:
            t, k, life, dt = "Entity", "person", None, None
        elif title in truth["orgs"]:
            t, k, life, dt = "Entity", "organization", None, None
        else:
            t, k, life, dt = "Document", "note", None, None
        notes[f"{VAULT}\0{rel}"] = {"type": t, "kind": k, "lifecycle": life, "lifecycle_evidence": None,
                                    "date": dt, "topics": [], "content_sha256": hashlib.sha256(text.encode()).hexdigest()}
    links = [{"source": f"{VAULT}\0{by_title[task]}", "target": f"{VAULT}\0{by_title[dec]}",
              "relationship": "implements", "evidence": None}
             for task, dec in json.loads((DATA / "implements.json").read_text())]
    sidecar = {"format": "native.enrichment.v1", "created_at": datetime.now(timezone.utc).isoformat(),
               "agent": {"cli": "ground-truth", "model": None}, "sources": [str(VAULT)], "notes": notes,
               "links": links, "amends": [], "supersession_candidates": [], "unenriched": [], "usage": {}}
    side = DATA / "enrichment.json"
    side.write_text(json.dumps(sidecar))

    if not links_only:
        out = subprocess.run([str(NATIVE), "import", "--db", str(DB), "--enrichment", str(side), str(VAULT)],
                             capture_output=True, text=True)
        print(out.stdout[-1500:], out.stderr[-1500:])
        if out.returncode:
            raise SystemExit("import failed")

    n = Native(DB)
    n.bootstrap()
    ids = {}
    # Only decisions: query_sql truncates large result sets, which silently dropped rows.
    rows = n.op("sql_read", "query_sql",
                {"sql": "SELECT id, name FROM records WHERE type = 'Resolution' ORDER BY id"})
    assert not rows.get("truncated"), "decision list truncated"
    for r in rows.get("rows", []):
        ids[r["name"] if isinstance(r, dict) else r[1]] = r["id"] if isinstance(r, dict) else r[0]
    ok = 0
    for newer, older in json.loads((DATA / "supersedes.json").read_text()):
        n.op("records_write", "manage_links.add",
             {"source_id": ids[newer], "target_id": ids[older], "relationship": "supersedes",
              "note": "Newer decision replaces older one (stated in its body)"})
        ok += 1
    print(f"supersedes links added: {ok}")
    n.close()


if __name__ == "__main__":
    main()
