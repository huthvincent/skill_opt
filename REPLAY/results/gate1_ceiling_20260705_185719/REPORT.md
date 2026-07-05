# REPORT - gate1_ceiling_20260705_185719

- started: 2026-07-05T18:57:19  finished: 2026-07-05T19:03:07
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
| B_optimizer_cost_usd | 0.388 |
| B_library_entries | 0 |
| C_success | 0.6 |
| C_episodes | 60 |
| C_errors | 0 |
| C_cost_usd | 5.91 |
| delta_pp | -10.0 |
| total_spend_usd | 12.11 |
| gate1_verdict | FAIL |

## Conclusion

Gate 1 FAIL: baseline 70.0% -> with-library 60.0% (-10.0pp, gate >= +10pp), spend ~$12.11 (+ untracked NL-judge calls ~$1).

## Per-task (baseline<1.0) paired success

| task | base | lib |
|---|---|---|
| 16 | 0.5 | 0.5 |
| 2 | 0.5 | 0.0 |
| 20 | 0.0 | 0.0 |
| 21 | 0.5 | 0.5 |
| 22 | 0.5 | 0.5 |
| 27 | 0.0 | 0.5 |
| 28 | 0.5 | 0.0 |
| 3 | 0.0 | 0.0 |
| 4 | 0.5 | 0.0 |
| 6 | 0.0 | 0.0 |
| 7 | 0.0 | 0.0 |
| 8 | 0.0 | 0.5 |

## Library used

see `library.md` in this run dir

