# Write benchmark results

36 trials from writes.jsonl. Reader model: gpt-5-mini.

Each trial: one agent files a week of messages into the workspace (5 decisions replaced, 2 task status changes, 1 new task, 2 distractors), then a fresh reader answers 9 questions against the result.

## Headline

| Model | Setup | Runs | Changes applied | Replacements recorded | Distractors kept out | Next agent correct | Tokens / trial (median) | Tokens per correct change | Failed tool calls (median) | Time (median) | Cost / trial |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-5-mini | markdown | 3 | 39/39 (100%) | 15/15 (100%) | 6/6 (100%) | 26/27 (96%) | 1506k | 99k | 1 | 206s | $0.121 |
| gpt-5-mini | native | 3 | 32/39 (82%) | 9/15 (60%) | 6/6 (100%) | 24/27 (89%) | 827k | 83k | 3 | 166s | $0.077 |
| gpt-5-mini | native_hinted | 3 | 39/39 (100%) | 15/15 (100%) | 6/6 (100%) | 23/27 (85%) | 891k | 64k | 1 | 143s | $0.071 |
| gpt-5-mini | native_combined | 3 | 39/39 (100%) | 15/15 (100%) | 6/6 (100%) | 23/27 (85%) | 959k | 74k | 1 | 161s | $0.075 |
| gpt-5-nano | markdown | 3 | 10/39 (26%) | 4/15 (27%) | 6/6 (100%) | 17/27 (63%) | 694k | 149k | 1 | 126s | $0.046 |
| gpt-5-nano | native | 3 | 7/39 (18%) | 0/15 (0%) | 5/6 (83%) | 11/27 (41%) | 278k | 134k | 12 | 68s | $0.034 |
| gpt-5-nano | native_hinted | 3 | 27/39 (69%) | 8/15 (53%) | 6/6 (100%) | 13/27 (48%) | 446k | 49k | 3 | 110s | $0.046 |
| gpt-5-nano | native_combined | 3 | 23/39 (59%) | 9/15 (60%) | 6/6 (100%) | 16/27 (59%) | 473k | 58k | 2 | 93s | $0.034 |
| gpt-5.6-luna | markdown | 3 | 39/39 (100%) | 15/15 (100%) | 6/6 (100%) | 26/27 (96%) | 385k | 29k | 0 | 60s | $0.164 |
| gpt-5.6-luna | native | 3 | 39/39 (100%) | 15/15 (100%) | 6/6 (100%) | 24/27 (89%) | 499k | 73k | 6 | 78s | $0.252 |
| gpt-5.6-luna | native_hinted | 3 | 39/39 (100%) | 15/15 (100%) | 6/6 (100%) | 21/27 (78%) | 349k | 28k | 0 | 52s | $0.165 |
| gpt-5.6-luna | native_combined | 3 | 39/39 (100%) | 15/15 (100%) | 6/6 (100%) | 23/27 (85%) | 158k | 20k | 0 | 44s | $0.139 |
| ALL | markdown | 9 | 88/117 (75%) | 34/45 (76%) | 18/18 (100%) | 69/81 (85%) | 694k | 74k | 1 | 126s | $0.110 |
| ALL | native | 9 | 78/117 (67%) | 24/45 (53%) | 17/18 (94%) | 59/81 (73%) | 588k | 83k | 5 | 98s | $0.121 |
| ALL | native_hinted | 9 | 105/117 (90%) | 38/45 (84%) | 18/18 (100%) | 57/81 (70%) | 512k | 47k | 1 | 110s | $0.094 |
| ALL | native_combined | 9 | 101/117 (86%) | 39/45 (87%) | 18/18 (100%) | 62/81 (77%) | 554k | 50k | 1 | 93s | $0.083 |

**Replacements recorded**: Native needs a typed `supersedes` link (or relationship) from the new record to the old decision; Markdown accepts any explicit marker a reader could use (the new note naming the old one with replace/supersede wording, or the old note edited to say it is superseded). The Markdown check is the more lenient one. **Next agent correct** is the setup-neutral test: a fresh reader answering questions about the new state.

## Per check (pass rate across runs)

| Check | gpt-5-mini markdown | gpt-5-mini native | gpt-5-mini native_hinted | gpt-5-mini native_combined | gpt-5-nano markdown | gpt-5-nano native | gpt-5-nano native_hinted | gpt-5-nano native_combined | gpt-5.6-luna markdown | gpt-5.6-luna native | gpt-5.6-luna native_hinted | gpt-5.6-luna native_combined |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D1_not_recorded | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D2_not_recorded | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R1_new_decision | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R1_replacement_recorded | 3/3 | 2/3 | 3/3 | 3/3 | 1/3 | 0/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R2_new_decision | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R2_replacement_recorded | 3/3 | 2/3 | 3/3 | 3/3 | 1/3 | 0/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R3_new_decision | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R3_replacement_recorded | 3/3 | 2/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R4_new_decision | 3/3 | 2/3 | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R4_replacement_recorded | 3/3 | 1/3 | 3/3 | 3/3 | 1/3 | 0/3 | 2/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R5_new_decision | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| R5_replacement_recorded | 3/3 | 2/3 | 3/3 | 3/3 | 1/3 | 0/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| T1_status | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| T2_status | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 0/3 | 2/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| T3_new_task | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 2/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| no_deletions | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

## How Native agents recorded replacements

| Model | Setup | Typed links | Prose only (no link) | Reversed link | New decision typed as Resolution | Task status in `lifecycle` field | Records without a name |
|---|---|---|---|---|---|---|---|
| gpt-5-mini | native | 9/15 | 5 | 0 | 14/15 | 0/6 | 0 |
| gpt-5-mini | native_hinted | 15/15 | 0 | 0 | 15/15 | 6/6 | 0 |
| gpt-5-mini | native_combined | 15/15 | 0 | 0 | 15/15 | 6/6 | 0 |
| gpt-5-nano | native | 0/15 | 3 | 0 | 5/15 | 0/6 | 0 |
| gpt-5-nano | native_hinted | 8/15 | 2 | 0 | 15/15 | 3/6 | 0 |
| gpt-5-nano | native_combined | 9/15 | 0 | 0 | 11/15 | 2/6 | 0 |
| gpt-5.6-luna | native | 15/15 | 0 | 0 | 15/15 | 6/6 | 0 |
| gpt-5.6-luna | native_hinted | 15/15 | 0 | 0 | 15/15 | 6/6 | 0 |
| gpt-5.6-luna | native_combined | 15/15 | 0 | 0 | 15/15 | 6/6 | 0 |

## Read-back, per question

| Question | gpt-5-mini markdown | gpt-5-mini native | gpt-5-mini native_hinted | gpt-5-mini native_combined | gpt-5-nano markdown | gpt-5-nano native | gpt-5-nano native_hinted | gpt-5-nano native_combined | gpt-5.6-luna markdown | gpt-5.6-luna native | gpt-5.6-luna native_hinted | gpt-5.6-luna native_combined |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Q2 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 1/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Q3 | 3/3 | 2/3 | 3/3 | 3/3 | 2/3 | 0/3 | 0/3 | 2/3 | 2/3 | 3/3 | 3/3 | 3/3 |
| Q4 | 2/3 | 1/3 | 3/3 | 3/3 | 2/3 | 0/3 | 1/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Q5 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Q6 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Q7 | 3/3 | 3/3 | 1/3 | 1/3 | 1/3 | 0/3 | 0/3 | 1/3 | 3/3 | 2/3 | 0/3 | 1/3 |
| Q8 | 3/3 | 3/3 | 1/3 | 1/3 | 2/3 | 0/3 | 0/3 | 0/3 | 3/3 | 1/3 | 0/3 | 1/3 |
| Q9 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
