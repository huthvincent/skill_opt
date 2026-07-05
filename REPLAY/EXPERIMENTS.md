# REPLAY 实验计划

> 每个计划中的实验先在这里登记（目的/配置/预算/状态），跑完后把 run_id 回填并在 `LEDGER.md` 记一行。状态：⬜计划 / 🔵进行 / ✅完成 / ❌废弃。

## E0 冒烟系列（阶段预算合计 ≤ $50，CONSTITUTION §6）

| ID | 目的 | 配置要点 | 预算 | 状态 | run_id |
|---|---|---|---|---|---|
| E0.0 | 零 LLM 结构探测：任务加载/事后 verifier/persona 注入/env 构建 | 无 LLM 调用 | $0 | ✅ | tau2_probe_20260705_043549 |
| E0.1 | τ²-bench 环境 + `shared/llm.py` 通路 + REPORT 自动生成全链路跑通 | retail 域 5 任务，agent=haiku 级，无经验库；注意 tau2 内部走 litellm，直接读 ANTHROPIC_API_KEY | ≤$5 | ⬜ | |
| E0.2 | "历史日志"生成管线 + 日志 schema 定稿 | 弱 agent × 3 persona，retail 域 30 session | ≤$15 | ⬜ | |
| E0.3 | 模块 A 提案质量人工检查 | E0.2 日志 → 失败聚类 → 候选条目，人工评 10 条 | ≤$10 | ⬜ | |
| E0.4 | replay 探针 test-retest 稳定性 | 同一决策点重放 ×5，测判定一致率 | ≤$10 | ⬜ | |

## E1 主实验系列（需 `Doc/budget_estimate.md` 审批后启动）

| ID | 目的 | 状态 |
|---|---|---|
| E1.1 | 核心对比表：同预算 B 下 REPLAY vs 5 个 baseline × 3 域（PROPOSAL §3.1） | ⬜ 待设计细化 |
| E1.2 | 预算-性能曲线（B ∈ {0.1, 0.25, 0.5, 1.0}×B_max） | ⬜ |
| E1.3 | Ablation ×5（PROPOSAL §3.1） | ⬜ |
| E1.4 | judge-hacking 背离诊断图 | ⬜ |
| E1.5 | WildChat 副线 | ⬜ |
