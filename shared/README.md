# shared/ —— 两篇论文共用代码

> 维护规则见根目录 `CONSTITUTION.md`。本目录改动会同时影响 REPLAY 和 WildLoop，改接口前先检查两边的调用点。

| 文件 | 职责 | 关键约定 |
|---|---|---|
| `paths.py` | 项目内全部路径常量 + `new_run_id()` | 其他任何文件不许出现绝对路径字面量 |
| `llm.py` | **唯一**的 LLM 调用入口，anthropic / bedrock / **mock** 三后端（`.env` 的 `LLM_BACKEND` 切换；mock 零成本，离线测管线用），内置计费累计与预算熔断（`CostTracker`） | 实验脚本不许直接 import anthropic/boto3；每个 run 必须传入带 `max_cost_usd` 的 tracker |
| `fetch_bib.py` | 从 arXiv API 抓权威 BibTeX，生成两篇论文的 `refs.bib` | 纯 stdlib；加新文献 = 改 `ARXIV_IDS` 后重跑；不许手改 refs.bib（手工条目放各自 latex/ 下的 `extra_refs.bib`） |
| `runharness.py` | run 目录契约的执行者：`Run(results_root, run_id, config)` 自动生成 config.json（含 git hash）/ log.txt / metrics.json / REPORT.md | 每个实验脚本必须用它，不许手搓 run 目录 |

## 用法速查

```bash
~/.local/bin/uv run python -m shared.llm --selftest   # 验证 LLM 通路（约 $0.001）
python3 shared/fetch_bib.py                            # 重新生成两份 refs.bib
```

## 现状 / 下一步

- 2026-07-05：初始版本。`llm.py` 只提供单轮 `chat()`；τ²-bench 的多轮 agent loop 封装等 REPLAY 冒烟阶段按需求加到这里（如果两篇都要用）或加到 `REPLAY/script/`（如果只有 REPLAY 用）。
- 待办：judge 集成（多 judge 投票 + 扰动）封装 `judge.py`，REPLAY 模块 B 开工时建。
