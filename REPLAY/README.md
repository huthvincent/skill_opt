# REPLAY —— 第一篇论文（进行中）

> *REPLAY: Textual Experience Replay for Training-Free Skill Optimization from Real Interaction Logs*
> 先读根目录 `CONSTITUTION.md`；方法正典在 [`PROPOSAL.md`](PROPOSAL.md)；实验计划在 [`EXPERIMENTS.md`](EXPERIMENTS.md)；实验台账在 [`LEDGER.md`](LEDGER.md)。

## 当前状态（最后更新：2026-07-05）

**阶段：骨架刚建好，冒烟验证未开始。**

## 下一步（按顺序）

1. ⬜ clone τ²-bench 到 `third_party/`，pin commit 并登记（见 `third_party/README.md`）
2. ⬜ `script/smoke_tau2.py`：单域（retail）5 任务，弱 agent（haiku、无经验库）跑通 rollout + judge 打分 + REPORT.md 自动生成，验证 `shared/llm.py` 通路与预算熔断
3. ⬜ `script/gen_logs_tau2.py`：弱 agent × ≥3 persona simulator 批量生成"历史日志"到 `data/generated_logs/`（隐藏 verifier 结果的日志 schema 在此脚本中定义）
4. ⬜ 模块 A 最小版（失败聚类 + 候选条目提案），人工检查提案质量
5. ⬜ replay 探针稳定性预实验（PROPOSAL §5 风险第 2 条）
6. ⬜ 写 `Doc/budget_estimate.md` 交 owner 审批 → 主实验

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
