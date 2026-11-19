# Product notes for Richard and George

From one day as a first-time user of the public Native snapshot, plus 443 benchmark trials across 5 OpenAI models. The full list with evidence is in [friction-log.md](friction-log.md). This page is the short version, ranked by how much each would move adoption.

## What's great (keep it)

- **The core bet holds up.** On questions that need the *current* answer or a two-step hop, Native was more accurate than a Markdown vault for every model that made mistakes. Overall: 97% vs 93% correct. Cheap models gained the most (gpt-5-mini went from 90% to 98% over two runs), and two-step questions went from 23/28 to 26/28 across models.
- **The repair envelopes are the best agent-facing errors I've used.** Every wrong call told the agent the exact fix, often with a ready-to-send `next_call`. No dead ends in 443 trials.
- **Import is fast and clean.** 2,497 Markdown notes and 639 wikilinks went in in about 50 seconds with zero unresolved links. The build takes 3 minutes.

## Top 5 fixes, ranked

1. **Default orientation costs more than the answer.** `bootstrap` returns ~41.6k characters, and most agents call it first. With a 4-line hint (skip bootstrap, don't pass `scope`, use the supersedes recipe), gpt-5.6-luna went from 79k to 14k tokens per correct answer at the same 100% accuracy. That turned Native from 2.7× *worse* than Markdown into 2.1× *better*.
   → Ship that hint as the default: a slim `bootstrap` profile for read-only Q&A, and put "skip bootstrap for simple questions" in the tool description.

2. **`search.scope` silently eats 29% of searches.** Models pass `scope: "all"` or `"workspace"`. It's a record ID, so the call errors, and OpenCode shows the error as an empty result.
   → Accept `all` / `workspace` / `*` as "no scope", or rename it to `subtree_id`.

3. **Payloads are about 9× the Markdown they replace.** `get_record` median is 8.2k characters against 0.9k for the same note as a file.
   → A `compact` / `fields` option that returns name, body, typed links and the supersedes chain.

4. **The README's "build an artifact" step is the hardest step.** It needs a "governed Collection" (undocumented), plan-gated grants, and 7+ calls. There's also no MCP guide topic for authoring artifacts.
   → One convenience operation that binds records or a SQL query to a new artifact and grants it, plus an `artifact-authoring` guide topic.

5. **Small API papercuts that each cost one round trip:** `reason` vs `note` vs `rationale`; `idempotency_key` required only on `manage_relationships.assert`; `records_read` rejecting operations it doesn't list directly; the SELF_HOSTING check calling a tool name that isn't listed.

## Things I'd build in the role (all open source, on the public engine)

1. **`native-bench`: this harness, maintained.** Your post says you're preparing to open-source a way to reproduce the benchmark and run private evals. This repo already runs Native vs Markdown across models and corpus sizes with one command, with a budget guard, and gives Native a public, rerunnable proof point. Next steps: add DeepSeek and Claude, plus your own corpus.
2. **A vault "freshness" importer.** It reads a Markdown vault, finds explicit "replaces [[X]]" / "superseded by" statements, and writes the `native.enrichment.v1` sidecar with those applied as `supersedes` links, so `native import` gives users the freshness win on day one. It only applies explicit statements, so no LLM is needed.
3. **One-command client setup.** `npx native-connect` (or a skill) that builds or downloads `mcp-stdio` and wires it into Claude Code, Codex and OpenCode with the slim-orientation hint. The OpenCode wiring has a sharp edge we hit (it trusts `$PWD` over cwd), which a recipe should handle.
