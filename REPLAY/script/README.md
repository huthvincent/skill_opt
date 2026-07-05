# REPLAY/script/ —— 实验脚本

规范（CONSTITUTION §2、§3）：
- 命名 `<task>_<action>.py` 全小写下划线；一次性探索脚本加 `scratch_` 前缀，跑完可删。
- 路径一律从 `shared.paths` 派生；LLM 调用一律走 `shared.llm.chat()` 并传入带 `max_cost_usd` 的 `CostTracker`。
- 每个脚本跑一次 = 一个 `results/<run_id>/`，内含 `config.json`（含 git commit hash）、`log.txt`、自动生成的 `REPORT.md`。
- 跑主实验前脚本必须已 commit。

## 脚本清单（新脚本必须在此登记）

| 脚本 | 职责 | 状态 |
|---|---|---|
| `tau2_probe.py` | E0.0：零 LLM 结构探测（任务加载、事后 verifier、persona 注入点、env 构建） | ✅ 2026-07-05 通过 |
| `smoke_tau2.py` | E0.1 冒烟：τ²-bench 单域跑通全链路 | ⬜ 待写（下一个） |
| `gen_logs_tau2.py` | E0.2：弱 agent × persona 生成"历史日志"（persona 全部自注入——E0.0 发现原生任务 persona 为空） | ⬜ 待写 |
