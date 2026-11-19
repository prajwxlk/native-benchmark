# Results

80 trials from hinted.jsonl.

## Headline: Markdown vs Native, per model

| Model | Arm | Correct | Tokens per correct answer | Median tokens / trial | Median steps | Median time | Cost per correct |
|---|---|---|---|---|---|---|---|
| gpt-5.6-luna | native_hinted | 20/20 (100%) | 14k | 13k | 3 | 10s | $0.0187 |
| gpt-5.6-terra | native_hinted | 20/20 (100%) | 11k | 12k | 3 | 9s | $0.0353 |
| gpt-5-mini | native_hinted | 19/20 (95%) | 35k | 33k | 4 | 30s | $0.0065 |
| gpt-5-nano | native_hinted | 17/20 (85%) | 26k | 20k | 3 | 33s | $0.0016 |
| ALL | native_hinted | 76/80 (95%) | 21k | 15k | 3 | 15s | $0.0162 |

## Token ratio (Markdown ÷ Native, tokens per correct answer)

| Model | All questions | Freshness | Lookup | Multi-hop | Accuracy MD → Native |
|---|---|---|---|---|---|
| gpt-5.6-luna | n/a | n/a | n/a | n/a | 0% → 0% |
| gpt-5.6-terra | n/a | n/a | n/a | n/a | 0% → 0% |
| gpt-5-mini | n/a | n/a | n/a | n/a | 0% → 0% |
| gpt-5-nano | n/a | n/a | n/a | n/a | 0% → 0% |
| ALL | n/a | n/a | n/a | n/a | 0% → 0% |

## Accuracy by question type

| Model | Arm | Freshness | Lookup | Multi-hop |
|---|---|---|---|---|
| gpt-5.6-luna | native_hinted | 10/10 | 6/6 | 4/4 |
| gpt-5.6-terra | native_hinted | 10/10 | 6/6 | 4/4 |
| gpt-5-mini | native_hinted | 10/10 | 5/6 | 4/4 |
| gpt-5-nano | native_hinted | 10/10 | 5/6 | 2/4 |
| ALL | native_hinted | 40/40 | 22/24 | 14/16 |

## Spend

| Model | USD |
|---|---|
| gpt-5.6-luna | $0.37 |
| gpt-5.6-terra | $0.71 |
| gpt-5-mini | $0.12 |
| gpt-5-nano | $0.03 |
| **Total** | **$1.23** |

## Tools used (trials that used each)

- **native_hinted**: native_records_read (63), native_sql_read (20), native_call_executor (14)

## Wrong answers (4)

| Trial | Expected | Got |
|---|---|---|
| gpt-5-mini · native_hinted · L04 | Maya Okafor | (no answer) |
| gpt-5-nano · native_hinted · L04 | Maya Okafor | (no answer) |
| gpt-5-nano · native_hinted · M01 | Kenji Watanabe, Sofia Marchetti | (no answer) |
| gpt-5-nano · native_hinted · M02 | Daniel Reyes, Kenji Watanabe | (no answer) |
