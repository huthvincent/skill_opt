# REPORT - smoke_tau2_20260705_105714

- started: 2026-07-05T10:57:14  finished: 2026-07-05T11:01:43
- git commit: `b05fd33`
- config: see `config.json`

## Metrics

| metric | value |
|---|---|
| tau2_exit_code | 0 |
| n_simulations | 5 |
| terminations | ['user_stop', 'user_stop', 'infrastructure_error', 'infrastructure_error', 'infrastructure_error'] |
| rewards | [1.0, 0.0, None, None, None] |
| success_rate | 1/5 |
| cost_per_episode_usd | [0.0803, 0.0854, 0, 0, 0] |
| total_cost_usd | 0.1657 |
| under_cap | True |

## Conclusion

E0.1 CHECK NEEDED: 2/5 episodes completed, success 1/5, total ~$0.17 (avg $0.083/episode, haiku all roles) - per-episode number seeds Doc/budget_estimate.md.
