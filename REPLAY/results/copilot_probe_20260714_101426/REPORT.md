# REPORT - copilot_probe_20260714_101426

- started: 2026-07-14T10:14:26  finished: 2026-07-14T10:15:18
- git commit: `25a08b8`
- config: see `config.json`

## Metrics

| metric | value |
|---|---|
| chat_ok | True |
| chat_reply | OK |
| chat_tokens | in=12 out=2 |

## Conclusion

E0.5 copilot probe [GO]: chat_ok=True, tau2_tool_calling_ok=None (model=gpt-4o). If tau2_tool_calling_ok is True, Copilot supports the domain function-calling tau2 needs -> viable for smoke/log-gen. Reproducibility caveat (rolling model versions) still bars it from headline E1 numbers.
