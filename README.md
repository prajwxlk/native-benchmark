# Native vs Markdown: an independent check across 5 OpenAI models

An independent, rerunnable test of [Native](https://www.withnative.ai/)'s [Markdown benchmark](https://www.withnative.ai/research-and-posts/markdown-context-benchmark).

**602 read runs and 36 write runs · 5 OpenAI models · 2 workspace sizes · $16.03 in API spend.**

## 1. What Native claims, and what we checked

Native is a database for AI agents. It replaces a folder of Markdown notes (like an Obsidian vault). Their pitch: an agent answering questions about your company uses about **40× fewer tokens** with Native than when it searches a folder of notes, and fails less often.

Their own test used one model (DeepSeek) on their own company data. **We re-ran the same kind of test on 5 OpenAI models with data where we know every correct answer.** It's an independent check.

Their test only covers reading. [Section 5](#5-the-write-side-can-agents-keep-it-current) adds the other half: when something changes, can an agent record it so the *next* agent gets it right?

## 2. How we benchmarked it

**Step 1: invent a company.** A script ([`bench/gen_corpus.py`](bench/gen_corpus.py)) generated "Fernwork", a fake 6-person startup with 10 weeks of notes: meetings, decisions, tasks, customer calls and daily logs. That's 333 notes, plus a 10× bigger version with 2,497 notes.

The trap built into the data: **16 decisions were later replaced.** For example, "SMS reminders go through Twilio" is replaced weeks later by "we're switching to Vonage". The old note is never edited, just like real life. Native's main selling point is that it knows which note is current.

**Step 2: write 20 questions with exact answers** ([`data/questions.json`](data/questions.json)).
- **10 freshness questions:** "We decided X. Is that still current?" These test whether the agent catches the replacement.
- **6 lookups:** "Where is Kenji Watanabe based?"
- **4 two-step questions:** "Who owns the task that implements our *current* pricing decision?" The agent has to find the current decision, then the task, then the owner.

**Step 3: give the same questions to the agent in three setups.**

| Setup | What the agent gets |
|---|---|
| **Markdown** | The folder of notes, plus tools to search and read files |
| **Native** | The same notes loaded into Native, and *only* Native's tools |
| **Native + hint** | Same as Native, plus 4 lines of tips in the prompt |

**Step 4: run it.** Every question went to every setup on 5 models, from cheapest to strongest: gpt-5-nano, gpt-5-mini, gpt-5.4-mini, gpt-5.6-luna and gpt-5.6-terra. That's **443 runs for $9.82.** Each run starts from a clean slate in OpenCode, the same agent tool Native used.

**Step 5: score it.** The answer counts as right only if it contains the exact correct facts. A script checks this; there's no AI judge. For each setup we also recorded **tokens used per correct answer**, the same measure Native uses.

## 3. What the hint was, and why it mattered

Reading the Native runs, we saw the agents wasting tokens in three ways:

1. **They called `bootstrap` first.** It's Native's "here's everything about this workspace" tool, and it returns about 42,000 characters every time, even for "where is Kenji based?"
2. **Their searches broke.** Models passed `scope: "all"`, but `scope` expects a record ID, so 29% of searches errored. The agent saw that as "no results" and kept searching.
3. **Records are big.** Opening one record returned about 9× more text than reading the same note as a file.

The hint told the agent four things:
- Skip bootstrap.
- Search with just the query; leave out `scope`.
- Replaced decisions have a "supersedes" link you can look up.
- Records are large, so only open the ones you need.

The hint is a stand-in for fixes Native could make in the product itself. It isn't a suggestion that users should write prompts like this.

## 4. The data

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/chart-base-dark.svg">
  <img alt="Bar chart of tokens per correct answer by model and setup. Native + hint is shortest for every model it ran on; default Native is longest for gpt-5.4-mini, luna and terra." src="docs/chart-base-light.svg">
</picture>

**Base corpus, % correct · tokens per correct answer (lower is better):**

| Model | Markdown | Native | Native + hint |
|---|---|---|---|
| gpt-5-nano (cheapest) | 88% · 62k | 92% · 49k | **100% · 28k** |
| gpt-5-mini | 90% · 57k | 98% · 35k | **100% · 34k** |
| gpt-5.4-mini | 95% · 52k | 100% · 82k | not run |
| gpt-5.6-luna | 100% · 29k | 100% · 79k | **100% · 14k** |
| gpt-5.6-terra (strongest) | 100% · 18k | 100% · 51k | **100% · 11k** |
| **Overall** | 93% · 47k | 97% · 55k | **100% · 22k** |

gpt-5-nano and gpt-5-mini ran each question twice on Markdown and Native; everything else ran once. "Overall" for Native + hint covers 4 models.

What that means:
- **Native is more accurate.** That's their claim, and it held. Weaker models benefit most, because Native hands them the "current" answer instead of making them work it out.
- **By default, Native cost *more* tokens.** Strong models are good at searching files, and Native's big default responses outweighed its advantage. Luna used 79k with Native against 29k with Markdown.
- **With the hint, Native won on both.** It got 100% right using about half the tokens of Markdown. Luna went from 79k to 14k.
- **Size matters.** On the 10× corpus, plain Native already beat Markdown for gpt-5-mini, with 1.8× fewer tokens. Bigger workspaces favor Native because its fixed startup cost gets spread out.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/chart-10x-dark.svg">
  <img alt="Bar chart for the 10× corpus. gpt-5-mini: Markdown 83k, Native 46k. gpt-5.6-luna: Markdown 38k, Native 92k." src="docs/chart-10x-light.svg">
</picture>

| 10× corpus (2,497 notes) | Markdown | Native (default) |
|---|---|---|
| gpt-5-mini | 90% · 83k | **100% · 46k** |
| gpt-5.6-luna | 100% · 38k | 100% · 92k |

By question type (all models, base corpus):

| | Markdown | Native | Native + hint |
|---|---|---|---|
| Freshness | 65/70 | 68/70 | 40/40 |
| Lookup | 42/42 | 42/42 | 24/24 |
| Two-step | 23/28 | 26/28 | 16/16 |

Raw tables: [`results/summary.md`](results/summary.md), [`results/summary-hinted.md`](results/summary-hinted.md), [`results/summary-scale10.md`](results/summary-scale10.md).

## 5. The write side: can agents keep it current?

Native's homepage now leads with "98% less stale context". That depends on writing, not reading: when a decision changes, an agent has to record the new one *and* mark the old one as replaced. So we tested that too.

**The test.** Each run gives an agent a week of new messages ([`data/writes/feed.md`](data/writes/feed.md)) and asks it to update the workspace. The messages contain:
- **5 decisions that replace older ones,** for example "SMS reminders move from Vonage to Sinch".
- **3 task changes:** one task finished, one no longer needed, one new.
- **2 traps:** a proposal nobody agreed to (switching to Zendesk), and a fact that's already recorded (the launch date).

A script then checks the end state against the known right answer ([`data/writes/scenarios.json`](data/writes/scenarios.json)). Is the new decision there? Is the old one marked as replaced? Are the task statuses right? Did the traps stay out? Was anything deleted? Finally, **a fresh agent answers 9 questions about the new state.** That's the real test: did the writes make the next agent right?

Three setups again. "Native + hint" here is a different, 5-line hint about *writing*: how to create a decision, add the `supersedes` link and set a task's status ([exact text below](#technical-details)). 3 models × 3 setups × 3 runs = 27 runs for $3.19.

**Changes applied correctly · tokens per correct change (lower is better):**

| Model | Markdown | Native | Native + hint |
|---|---|---|---|
| gpt-5-nano (cheapest) | 26% · 149k | 18% · 134k | **69% · 49k** |
| gpt-5-mini | 100% · 99k | 82% · 83k | **100% · 64k** |
| gpt-5.6-luna (strongest tested) | 100% · 29k | 100% · 73k | **100% · 28k** |

**Replacements marked with a `supersedes` link** (Native only; 5 per run × 3 runs):

| Model | Native | Native + hint |
|---|---|---|
| gpt-5-nano | 0/15 (3 more in prose only) | 8/15 (2 more in prose only) |
| gpt-5-mini | 9/15 (5 more in prose only) | **15/15** |
| gpt-5.6-luna | 15/15 | 15/15 |

**What the next agent got right** (all 3 models, 9 runs per setup):

| | Markdown | Native | Native + hint |
|---|---|---|---|
| Task-status questions (2 per run) | **15/18** | 9/18 | 2/18 |
| All other questions (7 per run) | 54/63 | 50/63 | **55/63** |
| Traps kept out (2 per run) | 18/18 | 17/18 | 18/18 |

**Why task status failed** (Native writers, by what they changed on the task):

| Writer changed | Next agent got the status right |
|---|---|
| Only the `lifecycle` field | 3 of 19 |
| `lifecycle` and the note text | 8 of 8 |

What that means:
- **Strong models write well in every setup.** luna made every change, every time. Default Native cost it 2.5× more tokens per change than Markdown; with the hint they were level.
- **Weaker models forget the link.** Native only knows a decision was replaced if the agent adds a `supersedes` link. Without the hint, gpt-5-mini often wrote "this supersedes the Vonage decision" in the text without adding the link, and gpt-5-nano never added one. Native's own data shows the same pattern: 52 links against 246 replacements written in prose. The hint fixed it for gpt-5-mini.
- **The traps worked as intended.** Only one run, gpt-5-nano on default Native, recorded the Zendesk proposal as a decision.
- **We found a status bug in imported notes.** After import, a task's status lives in three places: Native's `lifecycle` field, a copy of the note's frontmatter (`fm.status`), and the "Status:" line in the note text. Agents that set the proper field usually left the other two alone, and the next agent read the old status from the text. On every other question the setups were level.

The fixes on Native's side: on import, move the note's status into `lifecycle` and drop the duplicates. Also, let `create_record` take a `replaces` argument, so marking the old decision is part of creating the new one instead of a second step agents forget.

Raw tables: [`results/summary-writes.md`](results/summary-writes.md). What every agent actually wrote: `results/writes/<run>/`, with `changes.diff` for Markdown and `events.json` (Native's change log) for Native.

## 6. One hint for reading and writing

The read hint and the write hint were tested separately, but a real agent does both. So we merged them into one hint: the read hint, followed by the write hint's lines on creating records, linking replacements and setting status. The two tips they share are said once. Then we ran both benchmarks again with it. For a fair comparison we re-ran the read hint next to it, because these runs use a cleaner prompt than the earlier read runs ([details](#technical-details)). Cost: $3.02.

**Reading** (20 questions, 1 run each; % correct · tokens per correct answer):

| Model | Read hint | Combined hint |
|---|---|---|
| gpt-5-nano | 100% · 25k | 100% · 24k |
| gpt-5-mini | 100% · 30k | 100% · 28k |
| gpt-5.6-luna | 100% · 16k | 100% · 14k |
| gpt-5.6-terra | 100% · 12k | 100% · 10k |
| **Overall** | 100% · 21k | **100% · 19k** |

**Writing** (3 runs each; changes applied correctly · tokens per correct change):

| Model | Write hint | Combined hint |
|---|---|---|
| gpt-5-nano | 69% · 49k | 59% · 58k |
| gpt-5-mini | 100% · 64k | 100% · 74k |
| gpt-5.6-luna | 100% · 28k | **100% · 20k** |
| **Overall** | 90% · 47k | 86% · 50k |

**Writing, the other checks** (all 3 models, 9 runs per hint; Markdown for reference):

| | Write hint | Combined hint | Markdown |
|---|---|---|---|
| Replacements linked with `supersedes` | 38/45 | **39/45** | n/a |
| Traps kept out | 18/18 | 18/18 | 18/18 |
| Next agent: task-status questions | 2/18 | 5/18 | **15/18** |
| Next agent: all other questions | 55/63 | **57/63** | 54/63 |
| Next agent: total | 57/81 | 62/81 | **69/81** |

What that means:
- **One hint is enough.** The extra writing lines cost reading nothing: still 100% correct, with slightly fewer tokens on every model. On writing it matched the write-only hint within run-to-run noise. gpt-5-nano swings the most.
- **So Native could ship this as its default.** A block this short, in the tool descriptions or a slim `bootstrap`, would replace a 42,000-character orientation.
- **It doesn't fix the status bug.** Combined-hint writers also updated only `lifecycle`, so the next agent still missed most task-status questions. That needs the product fix from section 5, not a better prompt.
- **The cleaner prompt didn't change the read results.** The read hint scored 21k per correct answer now against 22k before, at 100% both times.

One read run (gpt-5-nano, read hint, question M03) hung at OpenCode startup four times in a row, before reaching the model. It's excluded as a harness fault, so that cell has 19 runs.

Raw tables: [`results/summary-combined-read.md`](results/summary-combined-read.md), [`results/summary-writes.md`](results/summary-writes.md).

## 7. Friction points

**Setup**
- The build was quick: 3 minutes and about 4 GB. That's a positive.
- The setup guide's first check (`engine_info`) fails if you follow it literally.
- Importing notes doesn't apply "this replaces that" automatically, so new users miss the main benefit.

**Using it as an agent**
- About 16k tokens of startup cost, mostly from `bootstrap`.
- The `scope` trap that empties 29% of searches.
- Responses are about 9× bigger than the notes they replace.
- The same "why" field has three names (`reason`, `note`, `rationale`) across different calls.
- Some read operations fail on the first try and only work through a side route (`call_executor`).
- A valid SQL query (`count(*)`) returns "not authorized".
- The README's showcase step, "build an artifact", is the hardest step and is undocumented. We couldn't finish it in 7 tries.
- One clear positive: the error messages are excellent. Every mistake told the agent exactly how to fix it.

## 8. The three things we'd build

1. **native-bench.** Native's post says they're planning to release a reproducible benchmark. This repo already runs with a single command across models, with a budget limit. We'd hand it over and maintain it.
2. **A "freshness" importer.** It reads your notes, finds explicit lines like "this replaces [[X]]", and links them as replacements during import. New users then get Native's main benefit on day one without any manual work.
3. **One-command setup: `npx native-connect`.** It installs Native and connects it to Claude Code, Codex or OpenCode with the slim defaults already applied.

The top fixes on Native's side:
- A slim `bootstrap`.
- Accepting `scope: "all"`.
- A compact record option.
- Accepting the same field name for "why" everywhere.

Those four product fixes would make the hint unnecessary. Ranked version: [findings/product-notes.md](findings/product-notes.md).

---

## Technical details

**How this differs from Native's benchmark**

| | Native's post | This repo |
|---|---|---|
| Data | their own event log, ~11k records, ~120 MB | synthetic, 333 or 2,497 notes |
| Models | DeepSeek v4.1 Flash (High effort) | 5 OpenAI models, default effort |
| Harness | OpenCode | OpenCode 1.18.3 |
| Runs | 3 per question | 1 (2 for nano and mini) |
| Markdown baseline | plain, wikilinks, Native-to-Markdown | wikilinks only |

**Loading Native.** [`bench/load_native.py`](bench/load_native.py) writes a `native.enrichment.v1` sidecar from the ground truth (record types, task lifecycle, task → decision `implements` links) and runs `native import --enrichment`. It then adds the 16 `supersedes` links over MCP, because import only lists them as candidates. Native gets perfect enrichment, so this tests retrieval, not enrichment quality.

**Isolation.** Each run gets a fresh OpenCode workspace outside any git repo, with its own config and data folders. The Markdown setup gets read-only bash, read, grep, glob and list. The Native setups get only Native's MCP tools (`mcp-stdio`, public snapshot `c4edccf`), with every built-in tool switched off.

**The exact hint text:**

> Tips: you do not need to call bootstrap. Search with records_read operation 'search' and arguments {query} only (scope is a record id, so omit it). A newer record that replaces an older one has a link with relationship 'supersedes' (see sql_read query_sql on the links and records tables). get_record payloads are large, so fetch only records you need.

**Write benchmark.** [`bench/gen_writes.py`](bench/gen_writes.py) builds the feed, the expected end state and the read-back questions from the same ground truth. [`bench/run_writes.py`](bench/run_writes.py) gives each writer a fresh copy of the vault or database. The Markdown writer also gets write and edit tools. Each run is then graded by script, and a fresh gpt-5-mini reader answers the read-back questions. Markdown is read by the Markdown reader. Both Native setups are read by the hinted Native reader, so read-back differences come from what was written, not from how it was read. Write runs switch off OpenCode's Claude Code compatibility layer, so no local agent instructions reach the model.

How "replacement recorded" is graded:
- **Native** needs a typed `supersedes` link from the new record to the old decision. Prose alone doesn't count, because Native's freshness features can't see it; it's reported separately as "prose only".
- **Markdown** accepts any explicit marker a reader could use: the new note naming the old one with "replaces" or "supersedes" wording, or the old note edited to say it's outdated. That's the more lenient check.

Task statuses pass if `lifecycle` or the `fm.status` copy is right in Native, or if the frontmatter or the "Status:" line is right in Markdown.

**The exact write hint:**

> Tips: you do not need to call bootstrap. Find records with records_read operation 'search' and arguments {query} only. Create records with records_write operation 'create_record' and arguments {type, kind, name, body, reason}: decisions are type 'Resolution' kind 'decision'; tasks are type 'WorkItem' kind 'task' with a lifecycle. Record that a new decision replaces an older one with records_write operation 'manage_links.add' and arguments {source_id: new id, target_id: old id, relationship: 'supersedes', note}. Change a task's status with records_write operation 'update_record' and arguments {id, lifecycle, reason}; lifecycle is one of open, in_progress, blocked, completed, closed.

**The combined hint** is the read hint above, followed by the write hint from "Create records…" onward. It's built in [`bench/run.py`](bench/run.py) (`HINT_COMBINED`) and used for both benchmarks.

**Prompt hygiene.** OpenCode's Claude Code compatibility layer loads the machine's global Claude Code instructions (`~/.claude/CLAUDE.md`) into every agent's prompt. The write runs and the combined-hint runs switch it off. The earlier read runs (sections 2–4) had it on, the same for every setup. Re-running the read hint without it moved tokens per correct answer from 22k to 21k, which suggests the effect is small. The Markdown and default-Native read runs haven't been re-run yet.

**Limits**
- **The write test is one small feed,** 10 changes over a week, run 3 times per model and setup. One nano Markdown run dumped every message into a single note. It scored 0 on our checks but 9 out of 9 on read-back, because in a small vault a dump is enough for the next reader. A bigger, messier workspace would punish that more.
- **Small workspaces.** Native's fixed startup cost matters much more here than at 120 MB. That's partly the point of the 10× run, but neither is their scale.
- **Mostly one run per question.** Differences on a single question are noisy; read the per-model totals.
- **Synthetic notes are cleaner than real ones,** and every replacement is stated explicitly, which helps grep.
- **The hint is a prompt,** not a shipped product change. It shows what better defaults could do; it doesn't prove a given implementation would match.
- **OpenCode shows MCP errors to the model as empty results.** That inflates the cost of the `scope` errors. A client that shows the error text would recover faster.

## Reproduce

Needs Rust (rustup), Python 3, OpenCode and an OpenAI key in `.env` (`OPENAI_API_KEY=...`, gitignored).

```bash
git clone --depth 1 https://github.com/withnative/native vendor/native
(cd vendor/native && cargo build --locked --bin mcp-stdio --bin native)
python3 -I bench/gen_corpus.py && python3 -I bench/load_native.py
python3 -I bench/gen_corpus.py --out data/scale10 --scale 10 && python3 -I bench/load_native.py --data=data/scale10
python3 -I bench/run.py --models gpt-5-mini --arms markdown native native_hinted --out results/mine.jsonl
python3 -I bench/summarize.py results/mine.jsonl
python3 -I bench/chart.py
```

`run.py` skips finished runs, so it can be rerun, and stops before the total in `results/*.jsonl` passes `--budget` (default $9.90).

The write benchmark:

```bash
python3 -I bench/gen_writes.py
python3 -I bench/run_writes.py --models gpt-5-mini --runs 1 --budget 15 --out results/writes-mine.jsonl
python3 -I bench/summarize_writes.py results/writes-mine.jsonl
```

**Harness gotcha** for anyone driving OpenCode from a script: it resolves the project folder from `$PWD`, not the process's working directory. An inherited `PWD` let our first "Native" agents grep the Markdown vault. `run.py` sets `PWD` per run and keeps workspaces outside any git repo.

## Files

- `bench/`: data generator, Native loader, MCP client, runner, summariser, chart script and price table, plus the write benchmark (`gen_writes.py`, `run_writes.py`, `summarize_writes.py`).
- `data/`: questions and ground truth. The vaults and databases are generated; rebuild them with the commands above. `data/writes/` holds the write benchmark's feed, expected end state and read-back questions.
- `results/*.jsonl`: one row per run, with tokens, steps, time, cost, answer and grade. `results/writes/` holds what each write run changed. `*-invalid.jsonl` files hold rows excluded for harness faults; they're kept so the spend total stays honest.
- `docs/`: the charts above (light and dark).
- `findings/`: [product notes](findings/product-notes.md) (short and ranked) and the [friction log](findings/friction-log.md) (16 findings with evidence).

Native's engine is AGPL-3.0 and isn't included here. This repo only calls its public binaries.
