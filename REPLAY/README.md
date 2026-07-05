# REPLAY —— 第一篇论文（进行中）

> *REPLAY: Textual Experience Replay for Training-Free Skill Optimization from Real Interaction Logs*
> 先读根目录 `CONSTITUTION.md`；方法正典在 [`PROPOSAL.md`](PROPOSAL.md)；实验计划在 [`EXPERIMENTS.md`](EXPERIMENTS.md)；实验台账在 [`LEDGER.md`](LEDGER.md)。

## 当前状态（最后更新：2026-07-05）

**阶段：E0.0 零成本结构探测已通过，协议四依赖全部确认。** 关键事实：事后 `evaluate_simulation()` 可对已存轨迹算 reward（隐藏 verifier 协议可行）；`PersonaConfig` 官方注入接口存在且原生任务 persona 为空（用户多样性完全自控）；tau2 内部走 litellm、直接读 `ANTHROPIC_API_KEY`。

## 下一步（按顺序）

1. ✅ ~~clone τ²-bench~~（pin `1901a30`，已入 uv 环境，Python 升 3.12）
2. ✅ ~~E0.0 结构探测~~（run: `tau2_probe_20260705_043549`）
3. ⬜ `script/smoke_tau2.py`（E0.1）：单域（retail）5 任务，弱 agent（haiku、无经验库）跑通 rollout + judge 打分 + REPORT.md，验证预算熔断。**≤$5，需 owner 点头再跑**
4. ⬜ `script/gen_logs_tau2.py`（E0.2）：弱 agent × ≥3 自注入 persona 批量生成"历史日志"到 `data/generated_logs/`（日志 schema 定稿于 `Doc/log_schema.md`）
5. ⬜ 模块 A 最小版（失败聚类 + 候选条目提案），人工检查提案质量（E0.3）
6. ⬜ replay 探针稳定性预实验（E0.4，PROPOSAL §5 风险第 2 条）
7. ⬜ 写 `Doc/budget_estimate.md` 交 owner 审批 → 主实验

## 目录索引

| 目录/文件 | 内容 |
|---|---|
| `PROPOSAL.md` | 方法设计正典（问题设定、模块 A/A'/B/C、实验协议、贡献、风险） |
| `EXPERIMENTS.md` | 实验逐个登记：目的/配置/预算/状态 |
| `LEDGER.md` | run 台账，每 run 一行 |
| `script/` | 实验脚本（规范见其 README） |
| `results/` | run 输出，`results/<run_id>/`（规范见其 README） |
| `Doc/` | 手写分析文档（预算估算、跨实验对比、审稿预案） |
| `latex/` | 论文源文件，`latexmk -pdf main.tex` 编译 |
