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

## The write side (27 more trials)

Agents filed a week of messages: 5 replaced decisions, 3 task changes and 2 traps. A fresh agent then answered questions about the result. Full numbers: [summary-writes.md](../results/summary-writes.md).

1. **Status drifts after import.** An imported task keeps its status in three places: `lifecycle`, the `fm.status` facet and the "Status:" line in the body. Agents that set `lifecycle` left the other two stale. The next agent then read the stale text and got the status right 3 times out of 19. When the writer also changed the text, it was right 8 out of 8.
   → On import, move frontmatter status into `lifecycle` and remove the duplicates, or render `lifecycle` above the body in `get_record`.
2. **Weaker models write "supersedes" in prose but don't add the link.** Without a hint, gpt-5-mini added the link 9 times out of 15 and gpt-5-nano never did. Your own data shows the same pattern (52 links against 246 prose supersessions). A 5-line hint took gpt-5-mini to 15 out of 15.
   → A `replaces` argument on `create_record`, so the link is part of creating the decision, plus a write recipe in the tool description.
3. **One short hint covers reading and writing.** The read hint plus the write lines kept reading at 100% (19k tokens per correct answer, against 21k for the read hint alone) and matched the write-only hint on writing. It can be one default block, not two. It doesn't fix item 1.
4. **Default writes cost more than Markdown, and the hint closes the gap.** gpt-5.6-luna used 73k tokens per correct change with default Native, 29k with Markdown and 28k with the hint. Same slim-orientation story as the read side.

## Things I'd build in the role (all open source, on the public engine)

1. **`native-bench`: this harness, maintained.** Your post says you're preparing to open-source a way to reproduce the benchmark and run private evals. This repo already runs Native vs Markdown across models and corpus sizes with one command, with a budget guard, and gives Native a public, rerunnable proof point. Next steps: add DeepSeek and Claude, plus your own corpus.
2. **A vault "freshness" importer.** It reads a Markdown vault, finds explicit "replaces [[X]]" / "superseded by" statements, and writes the `native.enrichment.v1` sidecar with those applied as `supersedes` links, so `native import` gives users the freshness win on day one. It only applies explicit statements, so no LLM is needed.
3. **One-command client setup.** `npx native-connect` (or a skill) that builds or downloads `mcp-stdio` and wires it into Claude Code, Codex and OpenCode with the slim-orientation hint. The OpenCode wiring has a sharp edge we hit (it trusts `$PWD` over cwd), which a recipe should handle.
