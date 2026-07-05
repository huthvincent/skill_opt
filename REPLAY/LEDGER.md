# REPLAY 实验台账

> 每个 run 一行，倒序追加。规则：跑完实验未登记 = 任务未完成（CONSTITUTION §5.3）。
> 格式：`run_id | 日期 | 对应实验ID | 一句话目的 | 关键指标 | 一句话结论 | 进论文?`

| run_id | 日期 | 实验 | 目的 | 关键指标 | 结论 | 进论文? |
|---|---|---|---|---|---|---|
| tau2_probe_20260705_043549 | 2026-07-05 | E0.0 | 零 LLM 验证协议四依赖 | retail=114/airline=50/telecom=114; persona 覆盖 0/114; reward_basis=DB×114+NL×112 | PASSED：事后 evaluate_simulation ✅、PersonaConfig 注入 ✅、env 无 LLM 可建 ✅ →隐藏 verifier 协议与 WildLoop 接地均可实现；persona 需全部自注入（可控性↑） | 否（基建） |
