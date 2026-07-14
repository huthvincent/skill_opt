# REPLAY —— 第一篇论文（进行中）

> *REPLAY: Textual Experience Replay for Training-Free Skill Optimization from Real Interaction Logs*
> 先读根目录 `CONSTITUTION.md`；方法正典在 [`PROPOSAL.md`](PROPOSAL.md)；实验计划在 [`EXPERIMENTS.md`](EXPERIMENTS.md)；实验台账在 [`LEDGER.md`](LEDGER.md)。

## 当前状态（最后更新：2026-07-14）

**阶段：E0.0/E0.1 通过 + E0.5 Copilot 后端可行性 GO。** 关键事实：事后 `evaluate_simulation()` 可对已存轨迹算 reward（隐藏 verifier 协议可行）；`PersonaConfig` 官方注入接口存在且原生任务 persona 为空（用户多样性完全自控）；tau2 内部走 litellm、直接读 `ANTHROPIC_API_KEY`，但有两处 gpt-4.1 硬编码需运行时 patch（见 `script/README.md`）；实测单集 ~$0.094（haiku 全角色），全论文预算外推见 `Doc/budget_estimate.md`（混合方案 ~$2,000）。**新增（E0.5）：`shared/llm.py` 现支持 `LLM_BACKEND=copilot`（litellm `github_copilot/`，用 Copilot 订阅额度、无按 token 计费、无 API key），实测 gpt-4o 可作 tau2 agent 跑通域 function-calling（retail reward=1.0）——绕开 Gate1 的余额耗尽痛点。三条限制：① 只能 pin 到滚动别名（如 `claude-haiku-4.5`），不能 pin 到精确版本 model（Anthropic 可 pin `claude-haiku-4-5-20251001`），适合冒烟/开发；② **Copilot 版 Claude 拒绝扮演 tau2 user simulator**（护栏所致，见 LEDGER _105916），故 Copilot 跑 tau2 须用 gpt 系、且与 Rui 的 Anthropic-haiku 基线不可比；③ litellm 路由以 `copilot-integration-id: vscode-chat`（编辑器身份）访问，与官方 copilot-cli/sdk 的 `copilot-developer-cli` 不同——同一 enterprise 主机但模型 roster/护栏可能不同（疑似 ② 成因）。**

## 下一步（按顺序）

1. ✅ ~~clone τ²-bench~~（pin `1901a30`，已入 uv 环境，Python 升 3.12）
2. ✅ ~~E0.0 结构探测~~（run: `tau2_probe_20260705_043549`）
3. ✅ ~~E0.1 全链路冒烟~~（run: `smoke_tau2_20260705_110319`，4/5 成功，累计 ~$0.96）
4. ✅ ~~E0.5 Copilot 后端可行性~~（run: `copilot_probe_20260714_101426`+`_101723`，GO）
5. ⬜ `script/gen_logs_tau2.py`（E0.2）：弱 agent × ≥3 自注入 persona 批量生成"历史日志"到 `data/generated_logs/`（日志 schema 定稿于 `Doc/log_schema.md`）；可用 copilot 后端零边际成本跑
6. ⬜ 模块 A 最小版（失败聚类 + 候选条目提案），人工检查提案质量（E0.3）
7. ⬜ replay 探针稳定性预实验（E0.4，PROPOSAL §5 风险第 2 条）
8. ⬜ 写 `Doc/budget_estimate.md` 交 owner 审批 → 主实验

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
