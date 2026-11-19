# Results

360 trials from pilot.jsonl, full.jsonl, repeat.jsonl, hinted.jsonl.

## Headline: Markdown vs Native, per model

| Model | Arm | Correct | Tokens per correct answer | Median tokens / trial | Median steps | Median time | Cost per correct |
|---|---|---|---|---|---|---|---|
| gpt-5-mini | markdown | 36/40 (90%) | 57k | 44k | 6 | 24s | $0.0074 |
| gpt-5-mini | native | 39/40 (98%) | 35k | 27k | 4 | 24s | $0.0061 |
| gpt-5-mini | native_hinted | 20/20 (100%) | 34k | 33k | 4 | 29s | $0.0063 |
| gpt-5.4-mini | markdown | 19/20 (95%) | 52k | 49k | 4 | 17s | $0.0202 |
| gpt-5.4-mini | native | 20/20 (100%) | 82k | 77k | 5 | 22s | $0.0264 |
| gpt-5-nano | markdown | 35/40 (88%) | 62k | 36k | 4 | 31s | $0.0024 |
| gpt-5-nano | native | 37/40 (92%) | 49k | 36k | 4 | 33s | $0.0022 |
| gpt-5-nano | native_hinted | 20/20 (100%) | 28k | 21k | 3 | 33s | $0.0015 |
| gpt-5.6-luna | markdown | 20/20 (100%) | 29k | 25k | 4 | 13s | $0.0276 |
| gpt-5.6-luna | native | 20/20 (100%) | 79k | 83k | 7 | 23s | $0.0487 |
| gpt-5.6-luna | native_hinted | 20/20 (100%) | 14k | 13k | 3 | 10s | $0.0187 |
| gpt-5.6-terra | markdown | 20/20 (100%) | 18k | 15k | 3 | 10s | $0.0532 |
| gpt-5.6-terra | native | 20/20 (100%) | 51k | 52k | 5 | 14s | $0.1013 |
| gpt-5.6-terra | native_hinted | 20/20 (100%) | 11k | 12k | 3 | 9s | $0.0353 |
| ALL | markdown | 130/140 (93%) | 47k | 31k | 4 | 20s | $0.0181 |
| ALL | native | 136/140 (97%) | 55k | 51k | 5 | 23s | $0.0283 |
| ALL | native_hinted | 80/80 (100%) | 22k | 18k | 3 | 15s | $0.0155 |

## Token ratio (Markdown ÷ Native, tokens per correct answer)

| Model | All questions | Freshness | Lookup | Multi-hop | Accuracy MD → Native |
|---|---|---|---|---|---|
| gpt-5-mini | 1.6× | 1.6× | 1.5× | 1.8× | 90% → 98% |
| gpt-5.4-mini | 0.6× | 0.7× | 0.5× | 0.7× | 95% → 100% |
| gpt-5-nano | 1.3× | 1.0× | 0.7× | 2.5× | 88% → 92% |
| gpt-5.6-luna | 0.4× | 0.4× | 0.3× | 0.5× | 100% → 100% |
| gpt-5.6-terra | 0.3× | 0.3× | 0.4× | 0.5× | 100% → 100% |
| ALL | 0.9× | 0.8× | 0.6× | 1.3× | 93% → 97% |

## Accuracy by question type

| Model | Arm | Freshness | Lookup | Multi-hop |
|---|---|---|---|---|
| gpt-5-mini | markdown | 17/20 | 12/12 | 7/8 |
| gpt-5-mini | native | 20/20 | 12/12 | 7/8 |
| gpt-5-mini | native_hinted | 10/10 | 6/6 | 4/4 |
| gpt-5.4-mini | markdown | 10/10 | 6/6 | 3/4 |
| gpt-5.4-mini | native | 10/10 | 6/6 | 4/4 |
| gpt-5.4-mini | native_hinted | – | – | – |
| gpt-5-nano | markdown | 18/20 | 12/12 | 5/8 |
| gpt-5-nano | native | 18/20 | 12/12 | 7/8 |
| gpt-5-nano | native_hinted | 10/10 | 6/6 | 4/4 |
| gpt-5.6-luna | markdown | 10/10 | 6/6 | 4/4 |
| gpt-5.6-luna | native | 10/10 | 6/6 | 4/4 |
| gpt-5.6-luna | native_hinted | 10/10 | 6/6 | 4/4 |
| gpt-5.6-terra | markdown | 10/10 | 6/6 | 4/4 |
| gpt-5.6-terra | native | 10/10 | 6/6 | 4/4 |
| gpt-5.6-terra | native_hinted | 10/10 | 6/6 | 4/4 |
| ALL | markdown | 65/70 | 42/42 | 23/28 |
| ALL | native | 68/70 | 42/42 | 26/28 |
| ALL | native_hinted | 40/40 | 24/24 | 16/16 |

## Spend

| Model | USD |
|---|---|
| gpt-5-mini | $0.63 |
| gpt-5.4-mini | $0.91 |
| gpt-5-nano | $0.20 |
| gpt-5.6-luna | $1.90 |
| gpt-5.6-terra | $3.80 |
| **Total** | **$7.44** |

## Tools used (trials that used each)

- **markdown**: grep (135), read (133), glob (103), bash (2)
- **native**: native_records_read (116), native_bootstrap (76), native_coordination_write (45), native_sql_read (31), native_call_executor (18), native_describe_operation (18), native_guidance_read (1)
- **native_hinted**: native_records_read (64), native_sql_read (20), native_call_executor (16)

## Wrong answers (14)

| Trial | Expected | Got |
|---|---|---|
| gpt-5-mini · markdown · F01 | £39 per clinic per month plus £2 per booking SMS | Not current — it's now £49 per clinic per month (unlimited seats). |
| gpt-5-mini · markdown · F01 | £39 per clinic per month plus £2 per booking SMS | No — current pricing is £49 per clinic per month, unlimited seats. |
| gpt-5-nano · native · F01 | £39 per clinic per month plus £2 per booking SMS | Not current. The latest Fernwork pricing in the notes is £49 per clinic per month, unlimited seats (as of 19 Nov 2026). |
| gpt-5-mini · markdown · F04 | Vonage | Twilio is no longer current; the SMS reminder provider is now MessageBird (decided 2026-09-06). |
| gpt-5-nano · markdown · F04 | Vonage | Not current. The sms reminder provider is MessageBird. |
| gpt-5-nano · native · F04 | Vonage | Yes, Twilio remains the SMS reminder provider. |
| gpt-5-nano · markdown · F05 | Gap Filler | Not current—the name is now Fill-in (the 2026-09-04 decision replaced the earlier Waitlist decision). |
| gpt-5-mini · markdown · M01 | Kenji Watanabe, Sofia Marchetti | Maya Okafor, Daniel Reyes |
| gpt-5-nano · markdown · M01 | Kenji Watanabe, Sofia Marchetti | Kenji Watanabe |
| gpt-5-nano · native · M01 | Kenji Watanabe, Sofia Marchetti | Kenji Watanabe |
| gpt-5-nano · markdown · M02 | Daniel Reyes, Kenji Watanabe | Kenji Watanabe; Tom Lindqvist |
| gpt-5.4-mini · markdown · M02 | Daniel Reyes, Kenji Watanabe | Tom Lindqvist; Kenji Watanabe |
| gpt-5-mini · native · M04 | Tom Lindqvist | (s) implementing our CURRENT name of the waitlist feature decision? Changed:  - n/a – no visible change Before/after: n/a – no visible change PR: n/a Verified:  |
| gpt-5-nano · markdown · M04 | Tom Lindqvist | Maya Okafor |
