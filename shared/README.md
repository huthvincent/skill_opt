# shared/ —— 两篇论文共用代码

> 维护规则见根目录 `CONSTITUTION.md`。本目录改动会同时影响 REPLAY 和 WildLoop，改接口前先检查两边的调用点。

| 文件 | 职责 | 关键约定 |
|---|---|---|
| `paths.py` | 项目内全部路径常量 + `new_run_id()` | 其他任何文件不许出现绝对路径字面量 |
| `llm.py` | **唯一**的 LLM 调用入口，anthropic / bedrock / **copilot** / **mock** 四后端（`.env` 的 `LLM_BACKEND` 切换；copilot=走 litellm `github_copilot/` 路由用 Copilot 订阅额度、无按 token 计费、首次触发设备流登录；mock 零成本离线测管线），内置计费累计与预算熔断（`CostTracker`；copilot 后端走 `add_flat` 只计 token/调用数不计 USD） | 实验脚本不许直接 import anthropic/boto3/litellm；每个 run 必须传入 tracker（付费后端配 `max_cost_usd`） |
| `fetch_bib.py` | 从 arXiv API 抓权威 BibTeX，生成两篇论文的 `refs.bib` | 纯 stdlib；加新文献 = 改 `ARXIV_IDS` 后重跑；不许手改 refs.bib（手工条目放各自 latex/ 下的 `extra_refs.bib`） |
| `runharness.py` | run 目录契约的执行者：`Run(results_root, run_id, config)` 自动生成 config.json（含 git hash）/ log.txt / metrics.json / REPORT.md | 每个实验脚本必须用它，不许手搓 run 目录 |

## 用法速查

```bash
~/.local/bin/uv run python -m shared.llm --selftest   # 验证 LLM 通路（约 $0.001）
python3 shared/fetch_bib.py                            # 重新生成两份 refs.bib
```

## 现状 / 下一步

- 2026-07-05：初始版本。`llm.py` 只提供单轮 `chat()`；τ²-bench 的多轮 agent loop 封装等 REPLAY 冒烟阶段按需求加到这里（如果两篇都要用）或加到 `REPLAY/script/`（如果只有 REPLAY 用）。
- 2026-07-14：`llm.py` 加 `copilot` 后端（litellm `github_copilot/` 路由，走 Copilot 订阅额度、无 API key、首次设备流登录、token 缓存 `~/.config/litellm/github_copilot/`）；`CostTracker` 加 `tokens_in/out` 字段 + `add_flat()`（flat-rate 后端只计 token/调用数）。E0.5 探针实测 tau2 agent 用 `github_copilot/gpt-4o` 可完成 retail 任务（reward=1.0），Copilot 支持 tau2 域工具的 function-calling。**三条限制**：(1) Copilot 只能 pin 到滚动别名（如 `claude-haiku-4.5`），不能 pin 到精确版本 model（Anthropic 可 pin `claude-haiku-4-5-20251001`），GitHub 会悄悄换权重，故仅适合冒烟/日志生成；(2) **Copilot 版 Claude 系模型不能作 tau2 user simulator**（服务层护栏使其拒绝角色扮演、自称"I'm Claude"死循环，见 LEDGER gate1_ceiling_20260714_105916）→ 跑 tau2 请用 gpt 系；(3) litellm 路由以 `copilot-integration-id: vscode-chat`（编辑器身份）访问，与官方 copilot-cli/sdk 的 `copilot-developer-cli` 不同——同一 enterprise 主机但模型 roster/护栏可能不同（疑似 (2) 成因）。
- 待办：judge 集成（多 judge 投票 + 扰动）封装 `judge.py`，REPLAY 模块 B 开工时建。
