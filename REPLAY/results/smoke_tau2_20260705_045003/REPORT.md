# REPORT - smoke_tau2_20260705_045003

- started: 2026-07-05T04:50:03  finished: 2026-07-05T04:54:35
- git commit: `b05fd33`
- config: see `config.json`

## Metrics

| metric | value |
|---|---|
| tau2_exit_code | 0 |
| n_simulations | 5 |
| terminations | ['user_stop', 'user_stop', 'infrastructure_error', 'infrastructure_error', 'infrastructure_error'] |
| rewards | [1.0, 1.0, None, None, None] |
| success_rate | 2/5 |
| cost_per_episode_usd | [0.0983, 0.0885, 0, 0, 0] |
| total_cost_usd | 0.1867 |
| under_cap | True |

## Conclusion

E0.1 CHECK NEEDED: 2/5 episodes completed, success 2/5, total ~$0.19 (avg $0.093/episode, haiku all roles) - per-episode number seeds Doc/budget_estimate.md.
