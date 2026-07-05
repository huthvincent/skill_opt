# REPORT - tau2_probe_20260705_043549

- started: 2026-07-05T04:35:49  finished: 2026-07-05T04:35:51
- git commit: `fc01842`
- config: see `config.json`

## Metrics

| metric | value |
|---|---|
| task_sets | mock,airline,retail,telecom_full,telecom_small,telecom,telecom-workflow,banking_knowledge |
| n_tasks_retail | 114 |
| n_tasks_airline | 50 |
| n_tasks_telecom | 114 |
| retail_persona_coverage | 0/114 |
| retail_reward_basis_dist | {'RewardType.DB': 114, 'RewardType.NL_ASSERTION': 112} |
| posthoc_eval_importable | True |
| evaluation_types | ['ENV', 'COMMUNICATE', 'ACTION', 'ALL', 'NL_ASSERTIONS', 'ALL_WITH_NL_ASSERTIONS', 'ALL_IGNORE_BASIS', 'ALL_WITH_NL_ASSERTIONS_IGNORE_BASIS'] |
| persona_config_injectable | True |
| env_constructible_no_llm | True |
| env_type | Environment |

## Conclusion

tau2-bench structure probe PASSED: task loading, post-hoc evaluate_simulation, and PersonaConfig injection all confirmed without any LLM call - hidden-verifier protocol and WildLoop grounding are implementable.
