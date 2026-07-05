# skill_Opt —— Training-Free Skill 优化论文项目

> **新来的 agent：先读 [`CONSTITUTION.md`](CONSTITUTION.md)，这是硬性规则。** 本文件只是总览。

## 项目当前状态（最后更新：2026-07-05）

| 事项 | 状态 |
|---|---|
| 文献调研（anchor 论文 + 38 篇周边 + 空白论证） | ✅ 完成，见 `docs/lit_survey_20260705.md` |
| 架构决策（12 项） | ✅ 完成，见 `docs/decisions_20260705.md` |
| 项目骨架 / uv 环境 / latex 骨架 | ✅ 本次搭建 |
| REPLAY 冒烟验证（τ²-bench 跑通 + 日志生成管线） | ⬜ 下一步 |
| REPLAY 主实验 | ⬜ 需先过预算审批（CONSTITUTION §6） |
| WildLoop | ⬜ 排队 |
| GitHub 私有远程 | ⬜ 待 owner 在交互终端完成 gh 认证 |

## 两篇论文

- **[`REPLAY/`](REPLAY/README.md)** — *REPLAY: Textual Experience Replay for Training-Free Skill Optimization from Real Interaction Logs*。核心主张：真实交互日志（off-policy、噪声隐式反馈）负责**提出**经验条目，小预算定向 on-policy rollout + 悲观门控负责**裁决**。目标 ICLR-27（约 2026-09-16 截稿）。
- **[`WildLoop/`](WildLoop/README.md)** — *WildLoop: 日志接地 user simulator 的优化-验证闭环 + WildLoop-Bench*。排队中，复用 REPLAY 的全部基础设施。

## 快速上手

```bash
cd /data2/zhu11/skill_Opt
~/.local/bin/uv sync                 # 装好 .venv（首次）
cp .env.example .env                 # 填入 API key（永不 commit）
~/.local/bin/uv run python -m shared.llm --selftest   # 验证 LLM 通路
cd REPLAY/latex && latexmk -pdf main.tex              # 编译论文 PDF
```

## 目录索引

| 目录 | 职责 | 维护文档 |
|---|---|---|
| `shared/` | 共用代码：LLM 双后端封装、路径、bib 工具 | `shared/README.md` |
| `data/` | 共享数据（raw 只读 + 生成的历史日志） | `data/README.md` |
| `third_party/` | 上游仓库 clone（τ²-bench 等） | `third_party/README.md` |
| `docs/` | 跨论文文档：文献调研、决策记录 | `docs/README.md` |
| `REPLAY/` | 第一篇论文全部内容 | `REPLAY/README.md` |
| `WildLoop/` | 第二篇论文全部内容 | `WildLoop/README.md` |
