# CONSTITUTION —— skill_Opt 项目宪法

> **任何 agent / 任何新任务开始前，必须先读完本文件，再读所属论文目录的 `README.md`，再读你要动的那个子目录的 `README.md`。三层都读完才准动手。**

本目录 `/data2/zhu11/skill_Opt/` 是"training-free skill/经验库优化"论文项目的根目录。项目 owner 不写代码，**文档就是 owner 对项目的全部可见性**——因此文档义务是硬性规则，不是建议。

---

## 0. 项目是什么（30 秒版）

两篇论文，共享一套基础设施：

| 论文 | 目录 | 一句话 | 状态 |
|---|---|---|---|
| **REPLAY** | `REPLAY/` | 文本空间的 offline-to-online RL：真实用户交互日志（噪声、off-policy）**提出**候选经验条目，定向 on-policy rollout + 悲观门控**裁决**是否入库，条目级 counterfactual 归因 | **进行中**，主攻 ICLR-27（约 2026-09-16） |
| **WildLoop** | `WildLoop/` | 日志接地 user simulator 的优化-验证闭环 + WildLoop-Bench benchmark | 排队，等 REPLAY 主实验跑通后启动 |

方法学背景、anchor 论文（SkillOpt / Training-Free GRPO / Skill-RM）、文献空白的完整论证见 `docs/lit_survey_20260705.md`；架构决策的来龙去脉见 `docs/decisions_20260705.md`。

---

## 1. 目录职责（一个目录 = 一个职责）

```
skill_Opt/
├── CONSTITUTION.md      ← 本文件。改规则必须经 owner 同意
├── README.md            ← 项目总览 + 当前状态 + 快速上手
├── CHANGELOG.md         ← 每次改动一行，倒序追加
├── .env / .env.example  ← API 凭证（.env 永不入 git）
├── pyproject.toml       ← 根级 uv 环境，两篇论文共用
│
├── shared/              ← 两篇论文共用的 python 代码（LLM 调用、路径、bib 工具）
├── data/                ← 共享数据。raw/ 只读；generated_logs/ 是弱 agent 造的"历史日志"
├── third_party/         ← 上游仓库 clone（τ²-bench 等），不改上游代码，patch 放各论文 script/
├── docs/                ← 跨论文文档：文献调研、架构决策、投稿时间线
│
├── REPLAY/              ← 第一篇论文（结构见 §2）
└── WildLoop/            ← 第二篇论文（同构）
```

**不要在根目录乱放散文件。** 新增顶层目录必须先问 owner。

## 2. 论文目录内部结构（两篇同构，移植自 owner 的 TB 项目规范）

```
REPLAY/
├── README.md        ← 该论文的维护文档：现状、下一步、目录索引（每次改动必须更新）
├── PROPOSAL.md      ← 方法设计正典。改方法必须先改这里并在 CHANGELOG 记录
├── EXPERIMENTS.md   ← 实验计划：每个实验的目的/配置/预算/状态
├── LEDGER.md        ← 实验台账：每个 run 一行（run_id | 日期 | 目的 | 关键指标 | 结论 | 是否进论文）
├── script/          ← 所有自写脚本。命名 <task>_<action>.py 全小写下划线；一次性探索脚本加 scratch_ 前缀
├── results/         ← 只放脚本自动输出。每次运行一个子目录 results/<run_id>/
├── Doc/             ← 人工撰写的长文档（设计讨论、跨实验分析、审稿回应草稿）
└── latex/           ← 论文源文件（main.tex + sections/ + refs.bib + figures/）
```

**`results/` vs `Doc/` 的边界**：`results/<run_id>/` 里的一切都是脚本自动生成、与该次运行强绑定；`Doc/` 是人（或 agent 受命）手写的、跨 run 的分析。

## 3. 命名与生成文件去向

- **run_id 格式**：`<script_name>_<YYYYMMDD_HHMMSS>`，例 `smoke_tau2_20260706_143000`。每执行一次脚本 = 一个新 run_id。
- **每个 run 目录必须包含**：
  - `config.json` —— 本次运行的全部参数（含模型名、温度、预算上限、git commit hash）
  - `log.txt` —— 运行日志
  - `REPORT.md` —— **脚本自动生成**的报告：配置摘要 + 指标表 + 一句话结论
  - 中间产物放 `results/<run_id>/cache/`，可删
- **路径常量写在脚本顶部**，且必须从 `shared/paths.py` 派生，例如：

```python
from shared.paths import PROJECT_ROOT, REPLAY_RESULTS
OUT_DIR = REPLAY_RESULTS / run_id   # 不允许出现 "/data2/zhu11" 字面量
```

## 4. 可移植性（硬约束——项目会被 clone 到另一台机器大规模跑）

Owner 会在另一台电脑 clone 本仓库、用 **AWS Bedrock 上的 Claude** 大规模跑实验。本机只负责"跑通"。因此：

1. **禁止硬编码绝对路径**。一切路径经 `shared/paths.py`（它自动探测项目根）。
2. **一切 LLM 调用必须走 `shared/llm.py`**，不允许在实验脚本里直接 import anthropic/boto3。后端由 `.env` 的 `LLM_BACKEND` 切换（`anthropic` = 直连 API，`bedrock` = AWS Bedrock），实验代码零改动迁移。
3. **大文件不入 git**：`data/`、`.venv/`、latex 编译产物都在 `.gitignore` 里。每个数据集在 `data/README.md` 里写清楚"如何重新下载/重新生成"（含命令），保证新机器可复原。
4. 新增依赖用 `~/.local/bin/uv add <pkg>`（会更新 pyproject.toml + uv.lock），不许 pip install 散装。

## 5. 严格模式：每个任务的文档义务（未完成 = 任务未完成）

每次改动（代码、文档、实验），收尾前必须做完：

1. **更新所在目录的 `README.md`**（如果改动影响了该目录的内容/用法/状态）；
2. **在根 `CHANGELOG.md` 顶部追加一行**：`- YYYY-MM-DD | <论文或 shared> | <一句话改了什么、为什么>`；
3. **跑了实验的**，在该论文 `LEDGER.md` 追加一行，并确认 `results/<run_id>/REPORT.md` 已生成；
4. **改了方法设计的**，同步更新 `PROPOSAL.md`（它是方法的唯一正典，代码与它冲突时以它为准并修代码）。

## 6. 预算纪律（分阶段审批制）

- 当前阶段：**冒烟验证，累计 API 花费上限 $50**。
- 每个实验脚本必须支持 `--max-cost-usd` 参数，`shared/llm.py` 内置计费累计，**触顶自动停**并在 REPORT.md 里注明。
- 进入主实验前，必须先产出一份预算估算文档（`REPLAY/Doc/budget_estimate.md`）交 owner 审批，批了才准跑。
- 任何单次 run 预期花费 > 当前阶段剩余额度 → 停下来问 owner，不许先跑再说。

## 7. Git 规则

- monorepo：整个 `skill_Opt/` 一个仓库。远程为 GitHub 私有仓库（配置好之前，至少保证本地 commit 频繁）。
- commit 信息格式：`[REPLAY|WildLoop|shared|docs] 一句话`，中文英文皆可。
- **永不 commit**：`.env`、`data/` 大文件、`results/**/cache/`、latex 编译产物。
- 实验代码在跑主实验前必须 commit（run 的 `config.json` 里记录 commit hash，保证可复现）。
- 里程碑（冒烟通过、主表跑完、投稿）打 tag。

## 8. 语言与写作规范

- 维护类文档（README/CHANGELOG/LEDGER/Doc）：**中文**。
- 代码、代码注释、论文 latex、git 里的英文皆可的场合：**英文**。
- 论文写作风格：主张必须有实验或引用支撑；`PROPOSAL.md` 中标注 `[待验证]` 的论断不许写进 latex 正文。

## 9. 安全红线

- `data/raw/` 只读，永不修改原始数据；需要清洗版本写到 `data/` 下新目录并在 README 登记。
- 永不删除 `results/` 下任何 run 目录（哪怕失败的 run 也是证据）；确要清理，列清单问 owner。
- 破坏性操作（rm -rf、git reset --hard、force push）一律先问 owner。
- API key 只存在 `.env`，不出现在任何代码、日志、commit、文档里。

## 10. Agent 开工检查清单（照抄执行）

```
[ ] 读完 CONSTITUTION.md（本文件）
[ ] 读所属论文的 README.md（了解现状和下一步）
[ ] 读要动的子目录的 README.md
[ ] 确认本任务预算影响（§6）
[ ] 干活
[ ] 文档义务四件套（§5）
[ ] git commit（§7）
```
