# Results

159 trials from combined-read.jsonl.

## Headline: Markdown vs Native, per model

| Model | Arm | Correct | Tokens per correct answer | Median tokens / trial | Median steps | Median time | Cost per correct |
|---|---|---|---|---|---|---|---|
| gpt-5-nano | native_hinted | 19/19 (100%) | 25k | 23k | 3 | 22s | $0.0012 |
| gpt-5-nano | native_combined | 20/20 (100%) | 24k | 20k | 3 | 19s | $0.0013 |
| gpt-5-mini | native_hinted | 20/20 (100%) | 30k | 28k | 4 | 20s | $0.0038 |
| gpt-5-mini | native_combined | 20/20 (100%) | 28k | 24k | 4 | 17s | $0.0036 |
| gpt-5.6-luna | native_hinted | 20/20 (100%) | 16k | 14k | 4 | 7s | $0.0190 |
| gpt-5.6-luna | native_combined | 20/20 (100%) | 14k | 12k | 3 | 7s | $0.0184 |
| gpt-5.6-terra | native_hinted | 20/20 (100%) | 12k | 11k | 3 | 6s | $0.0357 |
| gpt-5.6-terra | native_combined | 20/20 (100%) | 10k | 10k | 3 | 5s | $0.0305 |
| ALL | native_hinted | 79/79 (100%) | 21k | 18k | 3 | 10s | $0.0151 |
| ALL | native_combined | 80/80 (100%) | 19k | 17k | 3 | 10s | $0.0135 |

## Token ratio (Markdown ÷ Native, tokens per correct answer)

| Model | All questions | Freshness | Lookup | Multi-hop | Accuracy MD → Native |
|---|---|---|---|---|---|
| gpt-5-nano | n/a | n/a | n/a | n/a | 0% → 0% |
| gpt-5-mini | n/a | n/a | n/a | n/a | 0% → 0% |
| gpt-5.6-luna | n/a | n/a | n/a | n/a | 0% → 0% |
| gpt-5.6-terra | n/a | n/a | n/a | n/a | 0% → 0% |
| ALL | n/a | n/a | n/a | n/a | 0% → 0% |

## Accuracy by question type

| Model | Arm | Freshness | Lookup | Multi-hop |
|---|---|---|---|---|
| gpt-5-nano | native_hinted | 10/10 | 6/6 | 3/3 |
| gpt-5-nano | native_combined | 10/10 | 6/6 | 4/4 |
| gpt-5-mini | native_hinted | 10/10 | 6/6 | 4/4 |
| gpt-5-mini | native_combined | 10/10 | 6/6 | 4/4 |
| gpt-5.6-luna | native_hinted | 10/10 | 6/6 | 4/4 |
| gpt-5.6-luna | native_combined | 10/10 | 6/6 | 4/4 |
| gpt-5.6-terra | native_hinted | 10/10 | 6/6 | 4/4 |
| gpt-5.6-terra | native_combined | 10/10 | 6/6 | 4/4 |
| ALL | native_hinted | 40/40 | 24/24 | 15/15 |
| ALL | native_combined | 40/40 | 24/24 | 16/16 |

## Spend

| Model | USD |
|---|---|
| gpt-5-nano | $0.05 |
| gpt-5-mini | $0.15 |
| gpt-5.6-luna | $0.75 |
| gpt-5.6-terra | $1.33 |
| **Total** | **$2.27** |

## Tools used (trials that used each)

- **native_combined**: native_records_read (62), native_call_executor (18), native_sql_read (12)
- **native_hinted**: native_records_read (62), native_sql_read (27), native_call_executor (17)

## Wrong answers (0)

| Trial | Expected | Got |
|---|---|---|
