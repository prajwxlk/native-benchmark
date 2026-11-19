# Results

80 trials from scale10.jsonl.

## Headline: Markdown vs Native, per model

| Model | Arm | Correct | Tokens per correct answer | Median tokens / trial | Median steps | Median time | Cost per correct |
|---|---|---|---|---|---|---|---|
| gpt-5-mini | markdown | 18/20 (90%) | 83k | 75k | 6 | 20s | $0.0081 |
| gpt-5-mini | native | 20/20 (100%) | 46k | 29k | 4 | 16s | $0.0058 |
| gpt-5.6-luna | markdown | 20/20 (100%) | 38k | 34k | 4 | 16s | $0.0348 |
| gpt-5.6-luna | native | 20/20 (100%) | 92k | 98k | 7 | 25s | $0.0675 |
| ALL | markdown | 38/40 (95%) | 59k | 47k | 4 | 16s | $0.0221 |
| ALL | native | 40/40 (100%) | 69k | 67k | 6 | 21s | $0.0366 |

## Token ratio (Markdown ÷ Native, tokens per correct answer)

| Model | All questions | Freshness | Lookup | Multi-hop | Accuracy MD → Native |
|---|---|---|---|---|---|
| gpt-5-mini | 1.8× | 1.9× | 2.3× | 1.6× | 90% → 100% |
| gpt-5.6-luna | 0.4× | 0.3× | 0.5× | 0.5× | 100% → 100% |
| ALL | 0.9× | 0.9× | 0.9× | 0.9× | 95% → 100% |

## Accuracy by question type

| Model | Arm | Freshness | Lookup | Multi-hop |
|---|---|---|---|---|
| gpt-5-mini | markdown | 9/10 | 6/6 | 3/4 |
| gpt-5-mini | native | 10/10 | 6/6 | 4/4 |
| gpt-5.6-luna | markdown | 10/10 | 6/6 | 4/4 |
| gpt-5.6-luna | native | 10/10 | 6/6 | 4/4 |
| ALL | markdown | 19/20 | 12/12 | 7/8 |
| ALL | native | 20/20 | 12/12 | 8/8 |

## Spend

| Model | USD |
|---|---|
| gpt-5-mini | $0.26 |
| gpt-5.6-luna | $2.05 |
| **Total** | **$2.31** |

## Tools used (trials that used each)

- **native**: native_records_read (38), native_bootstrap (23), native_coordination_write (20), native_describe_operation (12), native_sql_read (6), native_call_executor (1)
- **markdown**: grep (40), read (40), glob (29)

## Wrong answers (2)

| Trial | Expected | Got |
|---|---|---|
| gpt-5-mini · markdown · F04 | Vonage | No — Twilio is no longer current; the SMS reminder provider is now MessageBird. |
| gpt-5-mini · markdown · M01 | Kenji Watanabe, Sofia Marchetti | Maya Okafor; Daniel Reyes |
