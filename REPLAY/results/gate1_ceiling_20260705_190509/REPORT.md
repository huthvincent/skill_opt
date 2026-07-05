# REPORT - gate1_ceiling_20260705_190509

- started: 2026-07-05T19:05:09  finished: 2026-07-05T19:09:22
- git commit: `27da204`
- config: see `config.json`

## Metrics

| metric | value |
|---|---|
| A_success | 0.7 |
| A_episodes | 60 |
| A_errors | 0 |
| A_cost_usd | 5.81 |
| projected_total_usd | 14.12 |
| A_failed_task_ids | ['16', '2', '20', '21', '22', '27', '28', '3', '4', '6', '7', '8'] |
| B_optimizer_cost_usd | 0.465 |
| B_library_entries | 16 |
| C_success | 0.579 |
| C_episodes | 38 |
| C_errors | 22 |
| C_cost_usd | 3.78 |
| delta_pp | -12.1 |
| total_spend_usd | 10.05 |
| gate1_verdict | FAIL |

## Conclusion

Gate 1 FAIL: baseline 70.0% -> with-library 57.9% (-12.1pp, gate >= +10pp), spend ~$10.05 (+ untracked NL-judge calls ~$1).

## Per-task (baseline<1.0) paired success

| task | base | lib |
|---|---|---|
| 16 | 0.5 | 0.0 |
| 2 | 0.5 | 0.0 |
| 20 | 0.0 | 1.0 |
| 21 | 0.5 | 1.0 |
| 22 | 0.5 | 0.0 |
| 27 | 0.0 | 1.0 |
| 28 | 0.5 | 1.0 |
| 3 | 0.0 | 0.0 |
| 4 | 0.5 | 0.0 |
| 6 | 0.0 | 0.0 |
| 7 | 0.0 | 0.0 |
| 8 | 0.0 | 0.0 |

## Library used

see `library.md` in this run dir

