# Native vs Markdown: an independent check across 5 OpenAI models

An independent, rerunnable test of [Native](https://www.withnative.ai/)'s claim that agents answer company-context questions with far fewer tokens and failures than with a Markdown vault ([their benchmark](https://www.withnative.ai/research-and-posts/markdown-context-benchmark)). It runs on a different model family (OpenAI), a synthetic corpus with known answers, and two corpus sizes.

**443 agent trials · 5 OpenAI models · 2 corpus sizes · $9.82 in API spend.**

## TL;DR

1. **Native is more accurate.** On the base corpus it got 97% right vs 93% for Markdown (136/140 vs 130/140), and 26/28 on two-step questions vs 23/28. Cheap models gained the most.
2. **By default, Native used *more* tokens on a small corpus** (55k vs 47k per correct answer). Strong models grep efficiently, while Native's defaults cost a lot per session: a ~41.6k-character `bootstrap`, ~9× larger record payloads, and 29% of searches lost to a `scope` mix-up.
3. **A 4-line hint that stands in for better defaults flips it.** With the hint, Native was 100% correct (80/80) at 22k tokens per correct answer. gpt-5.6-luna used 14k vs 29k for Markdown (2.1× fewer), and gpt-5.6-terra 11k vs 18k (1.6× fewer).
4. **Corpus size moves the crossover.** At 10× size, default Native already beat Markdown for gpt-5-mini (1.8× fewer tokens, 100% vs 90%), but not yet for gpt-5.6-luna (2.4× more).

## Results: base corpus (333 notes)

Accuracy and tokens per fully correct answer (lower is better).

| Model | Markdown | Native (default) | Native + hint |
|---|---|---|---|
| gpt-5-nano | 88% · 62k | 92% · 49k | **100% · 28k** |
| gpt-5-mini | 90% · 57k | 98% · 35k | **100% · 34k** |
| gpt-5.4-mini | 95% · 52k | 100% · 82k | not run |
| gpt-5.6-luna | 100% · 29k | 100% · 79k | **100% · 14k** |
| gpt-5.6-terra | 100% · 18k | 100% · 51k | **100% · 11k** |
| **All** | 93% · 47k | 97% · 55k | 100% · 22k¹ |

gpt-5-nano and gpt-5-mini: 2 runs × 20 questions on Markdown and Native. Everything else is 1 run × 20 questions.
¹ Four models; gpt-5.4-mini wasn't run with the hint.

| By question type (all models) | Markdown | Native | Native + hint |
|---|---|---|---|
| Freshness ("is X still current?") | 65/70 | 68/70 | 40/40 |
| Lookup | 42/42 | 42/42 | 24/24 |
| Two-step | 23/28 | 26/28 | 16/16 |

Median steps per trial: Markdown 4, Native 5, Native + hint 3. Cost per correct answer: $0.018, $0.028, $0.016.

## Results: 10× corpus (2,497 notes)

| Model | Markdown | Native (default) | Markdown ÷ Native tokens |
|---|---|---|---|
| gpt-5-mini | 90% · 83k | **100% · 46k** | 1.8× (Native cheaper) |
| gpt-5.6-luna | 100% · 38k | 100% · 92k | 0.4× (Markdown cheaper) |

Going from base to 10×, Markdown tokens per correct answer grew (gpt-5-mini 57k → 83k, luna 29k → 38k), while default Native stayed roughly flat for mini (35k → 46k). Native's fixed per-session cost is why its advantage needs scale, or slimmer defaults.

## Where Native's tokens go (from 140 default-Native traces)

| Cause | Evidence | Suggested fix |
|---|---|---|
| `bootstrap` orientation | called in 91 of 140 trials, often first; ~41.6k characters each time | slim `answer` profile (~2k characters) for read-only Q&A |
| Large payloads | `get_record` median 8.2k characters vs 0.9k for the same note read as a file; `search` p90 20k | `compact` / `fields` option |
| `search.scope` mix-up | 98 of 333 searches empty: models pass `scope: "all"`; it's a record id, so the call errors (shown by OpenCode as empty) | treat `all`/`workspace` as no scope, or rename to `subtree_id` |

Details and 13 more findings from setup and use: [findings/friction-log.md](findings/friction-log.md). Short ranked version: [findings/product-notes.md](findings/product-notes.md). Raw tables: [`results/summary.md`](results/summary.md), [`results/summary-scale10.md`](results/summary-scale10.md).

## Method

**Corpus.** [`bench/gen_corpus.py`](bench/gen_corpus.py) generates "Fernwork", a fake 6-person startup over 10 weeks, from a fixed seed: decisions, tasks, people, organisations, weekly meetings, customer calls and daily logs. 16 of 31 decisions are later replaced, some twice. Old notes are never edited: the newer decision says "This replaces [[X]]", like real notes. Meetings, calls and logs mention old values as distractors.
- **Base:** 333 notes, 244 KB.
- **10×:** 2,497 notes, 2 MB, with identical decisions, tasks, questions and answers (`--scale 10`).

**Questions.** 20 with exact answer keys ([`data/questions.json`](data/questions.json)):
- 10 freshness questions: "X was decided as Y. Is that still current? If not, what is it now?"
- 6 lookups: contact, role, city, vendor.
- 4 two-step questions: "who owns the task(s) implementing our CURRENT X decision?"

**Setups.** Each trial runs in a fresh, isolated OpenCode 1.18.3 workspace outside any git repo, with its own config and data directories:

| Setup | Tools the agent gets | Data |
|---|---|---|
| `markdown` | bash, read, grep, glob, list (read-only) | the vault folder (`[[wikilinks]]`) |
| `native` | only Native's MCP tools (`mcp-stdio`, public snapshot `c4edccf`); every built-in off and denied | the same vault, loaded with `native import` + typed `supersedes` / `implements` links |
| `native_hinted` | same as `native` | same, plus a 4-line hint in the prompt (below) |

The `native_hinted` prompt adds: *skip bootstrap; search with `{query}` only (scope is a record id); newer records have a `supersedes` link (use `query_sql` on `links`/`records`); `get_record` payloads are large, so fetch only what you need.* It stands in for product-side defaults; it isn't a claim that users should write prompts like this.

**Loading Native.** [`bench/load_native.py`](bench/load_native.py) writes a `native.enrichment.v1` sidecar from ground truth (record types, task lifecycle, task → decision `implements`) and runs `native import --enrichment`. It then asserts the 16 `supersedes` links over MCP, because import only lists supersession candidates. This gives Native perfect enrichment; we're testing retrieval, not enrichment quality.

**Models.** gpt-5-nano, gpt-5-mini, gpt-5.4-mini, gpt-5.6-luna and gpt-5.6-terra, at default reasoning effort, one run per question. gpt-5-nano and gpt-5-mini got a second run on Markdown and Native.

**Grading.** Deterministic: the final `ANSWER:` line must contain the answer key's distinctive substrings ([`bench/gen_corpus.py`](bench/gen_corpus.py) `key_for`). No LLM judge.

**Metrics** (as in Native's post): tokens per fully correct answer (all tokens ÷ correct answers), failed trials, median steps and time, plus cost per correct answer at list prices.

## How this differs from Native's benchmark

| | Native's post | This repo |
|---|---|---|
| Data | their own event log, ~11k records, ~120 MB | synthetic, 333 or 2,497 notes |
| Models | DeepSeek v4.1 Flash (High effort) | 5 OpenAI models, default effort |
| Harness | OpenCode | OpenCode 1.18.3 |
| Runs | 3 per question | 1 (2 for nano and mini) |
| Markdown baseline | plain, wikilinks, Native-to-Markdown | wikilinks only |

## Limits

- **Small corpora.** Native's fixed per-session cost matters much more here than at 120 MB. That's partly the point of the 10× run, but neither is their scale.
- **Mostly one run per question.** Single-question differences are noisy; read the model-level totals.
- **Synthetic notes are cleaner than real ones,** and every replacement is stated explicitly, which helps grep.
- **The hint is a prompt,** not a shipped product change. It shows what better defaults could do; it doesn't prove a given implementation would match.
- **OpenCode shows MCP errors to the model as empty results.** That inflates the cost of Native's `scope` errors. A client that surfaces error text would recover faster.

## Reproduce

Needs Rust (rustup), Python 3, OpenCode and an OpenAI key in `.env` (`OPENAI_API_KEY=...`, gitignored).

```bash
git clone --depth 1 https://github.com/withnative/native vendor/native
(cd vendor/native && cargo build --locked --bin mcp-stdio --bin native)
python3 -I bench/gen_corpus.py && python3 -I bench/load_native.py
python3 -I bench/gen_corpus.py --out data/scale10 --scale 10 && python3 -I bench/load_native.py --data=data/scale10
python3 -I bench/run.py --models gpt-5-mini --arms markdown native native_hinted --out results/mine.jsonl
python3 -I bench/summarize.py results/mine.jsonl
```

`run.py` skips finished trials, so it can be rerun, and stops before the total in `results/*.jsonl` passes `--budget` (default $9.90).

**Harness gotcha** for anyone driving OpenCode from a script: it resolves the project directory from `$PWD`, not the process cwd. An inherited `PWD` let our first "Native" agents grep the Markdown vault. `run.py` sets `PWD` per trial and keeps workspaces outside any git repo.

## Files

- `bench/`: generator, Native loader, MCP client, runner, summariser, price table.
- `data/`: questions and ground truth. The vaults and DBs are generated; regenerate them with the commands above.
- `results/*.jsonl`: one row per trial, with tokens, steps, time, cost, answer and grade. `*-invalid.jsonl` holds rows excluded for harness faults (kept so spend stays honest).
- `findings/`: [product notes](findings/product-notes.md) (short and ranked) and the [friction log](findings/friction-log.md) (16 findings with evidence).

Native's engine is AGPL-3.0 and isn't included here. This repo only calls its public binaries.
