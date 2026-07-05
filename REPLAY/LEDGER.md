# REPLAY 实验台账

> 每个 run 一行，倒序追加。规则：跑完实验未登记 = 任务未完成（CONSTITUTION §5.3）。
> 格式：`run_id | 日期 | 对应实验ID | 一句话目的 | 关键指标 | 一句话结论 | 进论文?`

| run_id | 日期 | 实验 | 目的 | 关键指标 | 结论 | 进论文? |
|---|---|---|---|---|---|---|
| gate1_ceiling_20260705_185719 | 2026-07-05 | Gate1 | 天花板测试(续跑B+C) | A=70% C=60% "-10pp" | **判定无效**：fable-5 推理耗尽 max_tokens=1200 输出空库(0字节), chat() 静默返回 → C 实测"空库vs基线"=纯运行噪声。**副产品发现: n=60 时同条件重跑方差可达 ±10pp**, gate 判读需配对+更谨慎 | 否 |
| gate1_ceiling_20260705_185023 | 2026-07-05 | Gate1 | 天花板测试(首跑) | 基线 A=70% (60集, $5.81, 0错误); 30题中12题有失败 | Phase A 完好可复用; Phase B 崩于 fable-5 拒收 temperature 参数(已修 llm.py) | 基线可复用 |
| smoke_tau2_20260705_110319 | 2026-07-05 | E0.1 | 全链路冒烟(修复后) | 5/5 完成; 成功 4/5; $0.094/集(haiku 全角色); 本轮 $0.47 | **PASSED**：tau2+Claude 全链路通; 单集成本实测入 budget_estimate; E0.1 系列累计 ~$0.96 | 否（基建） |
| smoke_tau2_20260705_105714 | 2026-07-05 | E0.1 | 诊断#2 | 2/5 完成; NL 判卷 JSON 解析失败 | 定位: haiku 判卷回复带 markdown 栏, json.loads 裸解析失败 → 加宽容 JSON shim | 否 |
| smoke_tau2_20260705_044317 | 2026-07-05 | E0.1 | 诊断#1 | 2/5 完成; 3 个 infrastructure_error | 定位: tau2 硬编码 gpt-4.1 做 NL_ASSERTIONS 判卷(无 CLI 开关) → 运行时 patch 模块常量 | 否 |
| tau2_probe_20260705_043549 | 2026-07-05 | E0.0 | 零 LLM 验证协议四依赖 | retail=114/airline=50/telecom=114; persona 覆盖 0/114; reward_basis=DB×114+NL×112 | PASSED：事后 evaluate_simulation ✅、PersonaConfig 注入 ✅、env 无 LLM 可建 ✅ →隐藏 verifier 协议与 WildLoop 接地均可实现；persona 需全部自注入（可控性↑） | 否（基建） |
