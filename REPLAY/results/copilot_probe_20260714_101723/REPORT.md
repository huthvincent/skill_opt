# REPORT - copilot_probe_20260714_101723

- started: 2026-07-14T10:17:23  finished: 2026-07-14T10:17:55
- git commit: `25a08b8`
- config: see `config.json`

## Metrics

| metric | value |
|---|---|
| tau2_exit_code | 0 |
| tau2_ran | True |
| tau2_n_simulations | 1 |
| tau2_terminations | ['user_stop'] |
| tau2_rewards | [1.0] |
| tau2_tool_calling_ok | True |

## Conclusion

E0.5 copilot probe [GO]: chat_ok=None, tau2_tool_calling_ok=True (model=gpt-4o). If tau2_tool_calling_ok is True, Copilot supports the domain function-calling tau2 needs -> viable for smoke/log-gen. Reproducibility caveat (rolling model versions) still bars it from headline E1 numbers.
