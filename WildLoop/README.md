# WildLoop —— 第二篇论文（排队中）

> *WildLoop: Closing the Loop between Real Interaction Logs and User Simulators for Skill Optimization*（+ 配套 WildLoop-Bench）
> 先读根目录 `CONSTITUTION.md`。方法构想见 [`PROPOSAL.md`](PROPOSAL.md)。

## 当前状态（最后更新：2026-07-05）

**排队中，未开工。** 启动条件：REPLAY 冒烟系列（E0.x）跑通——WildLoop 复用其全部基础设施（`shared/llm.py`、日志生成管线、judge 封装、τ²-bench 接入）。

## 与 REPLAY 的关系

- REPLAY 回答"怎么用日志优化经验库"；WildLoop 回答"怎么让优化所依赖的 simulator 忠于真实用户，并把这个闭环做成可复用的 benchmark"。
- 目录结构与 REPLAY 完全同构（script/results/Doc/latex + EXPERIMENTS + LEDGER，开工时补齐 EXPERIMENTS.md）。
- 预期投稿：REPLAY 之后的下一个 cycle（ARR 2026-10-12 或 ICLR-27 rebuttal 期后评估）。
