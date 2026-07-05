# REPLAY 实验计划

> 每个计划中的实验先在这里登记（目的/配置/预算/状态），跑完后把 run_id 回填并在 `LEDGER.md` 记一行。状态：⬜计划 / 🔵进行 / ✅完成 / ❌废弃。

## E0 冒烟系列（阶段预算合计 ≤ $50，CONSTITUTION §6）

| ID | 目的 | 配置要点 | 预算 | 状态 | run_id |
|---|---|---|---|---|---|
| E0.0 | 零 LLM 结构探测：任务加载/事后 verifier/persona 注入/env 构建 | 无 LLM 调用 | $0 | ✅ | tau2_probe_20260705_043549 |
| E0.1 | τ²-bench 环境 + `shared/llm.py` 通路 + REPORT 自动生成全链路跑通 | retail 域 5 任务，agent=haiku 级，无经验库；tau2 内部走 litellm 直接读 ANTHROPIC_API_KEY；**两处运行时 patch**（NL 判卷模型 gpt-4.1→haiku、宽容 JSON 解析），见 smoke_tau2.py 注释 | 实际 ~$0.96（含 2 轮诊断） | ✅ | smoke_tau2_20260705_110319 |
| E0.2 | "历史日志"生成管线 + 日志 schema 定稿 | 弱 agent × 3 persona，retail 域 30 session | ≤$15 | ⬜ | |
| E0.3 | 模块 A 提案质量人工检查 | E0.2 日志 → 失败聚类 → 候选条目，人工评 10 条 | ≤$10 | ⬜ | |
| E0.4 | replay 探针 test-retest 稳定性 | 同一决策点重放 ×5，测判定一致率 | ≤$10 | ⬜ | |

## Sanity Check 系列（`docs/sanity_check.md`，owner 批准 Gate 1 预算 ~$12 / 硬顶 $20）

| ID | 目的 | 配置要点 | 预算 | 状态 | run_id |
|---|---|---|---|---|---|
| Gate 1 | 天花板：好经验库到底有没有用（≥+10pp 过） | retail 30 题 × 2 trial × {无库, 强库}；强库由 optimizer 看失败轨迹+gold criteria 生成（允许作弊但禁任务专属 ID）；haiku 全角色 | 设计 ~$13 / 硬顶 $20；**实花 ~$18.4 触帽** | ⛔ **中断：API 账户余额耗尽**。3 次尝试均未获干净判定（fable 空库 bug → 余额耗尽污染）；沉淀资产：干净基线 A=70%(n=60)、12 条高质量天花板库、n=60 噪声带 ±10pp 实测。待充值后按 owner 选的方案重测 | gate1_ceiling_20260705_{185023,185719,190509} |

## E1 主实验系列（需 `Doc/budget_estimate.md` 审批后启动）

| ID | 目的 | 状态 |
|---|---|---|
| E1.1 | 核心对比表：同预算 B 下 REPLAY vs 5 个 baseline × 3 域（PROPOSAL §3.1） | ⬜ 待设计细化 |
| E1.2 | 预算-性能曲线（B ∈ {0.1, 0.25, 0.5, 1.0}×B_max） | ⬜ |
| E1.3 | Ablation ×5（PROPOSAL §3.1） | ⬜ |
| E1.4 | judge-hacking 背离诊断图 | ⬜ |
| E1.5 | WildChat 副线 | ⬜ |
