# 架构与研究决策记录（2026-07-05）

Owner 逐项拍板的 12 个决策。改变任何一条需 owner 同意并在此追加修订记录。

## 研究定位（ideation 阶段决策）

| # | 决策点 | 结论 |
|---|---|---|
| R1 | Skill 形式 | **文本经验库条目**（TF-GRPO / ExpeL 式），非 SKILL.md 文档、非代码技能 |
| R2 | 实验场景 | **标准 agent benchmark（τ²-bench）+ 公开真实对话日志（WildChat/LMSYS）** 双轨 |
| R3 | 训练成分 | **纯 training-free**，agent/optimizer/judge 全 API，不训任何参数 |
| R4 | 投稿目标 | 放弃 AAAI-27（摘要 2026-07-21 太紧），**主攻 ICLR-27（约 2026-09-16，官方未确认）**；backup：ARR 2026-10-12 |
| R5 | 论文拆分 | Idea A（离线提案+在线裁决）+ B（悲观门控）+ C（条目级归因）合并为 **REPLAY**；Idea D（simulator 闭环+benchmark）单独为 **WildLoop** |

## 工程架构（12 问答案）

| # | 决策点 | 结论 | 关键理由 |
|---|---|---|---|
| 1 | 第一篇命名 | **REPLAY** | owner 选定；呼应 RL 的 experience replay，方法本质即"文本空间经验回放" |
| 2 | 第二篇命名 | **WildLoop**（benchmark 叫 WildLoop-Bench） | WildChat 接地 + 闭环，一名全覆盖 |
| 3 | 仓库策略 | **monorepo + GitHub 私有远程** | 服务器单点，需容灾；gh 未装，待 owner 交互认证后配 remote |
| 4 | Python 环境 | **根目录单一 uv 环境**（uv 在 `~/.local/bin/uv`） | 依赖轻，两篇共用；沿 TS_Trading 的 uv 习惯 |
| 5 | LaTeX 流程 | **仓库为源 + 服务器 latexmk 本地编译**；协作时打包上 Overleaf | TeX Live 全套已装 |
| 6 | LaTeX 模板 | **通用 arXiv preprint 起手**，venue 定稿前再换 | ICLR-27 模板未发布 |
| 7 | run 规范 | **移植 TB 项目那套**：script/results/Doc 分离 + run_id=`<script>_<YYYYMMDD_HHMMSS>` + 每目录 README | owner 已有心智模型，零学习成本 |
| 8 | 结果追踪 | **纯文件系统**：每 run 自动 REPORT.md + 每论文 LEDGER.md 台账；不用 wandb | run 数量不大，避免平台依赖 |
| 9 | API 资源 | **Anthropic Claude**；本机直连 API 只求跑通，**大规模实验在另一台机器上走 AWS Bedrock Claude** | ⇒ 硬性可移植要求：路径经 shared/paths.py、LLM 调用经 shared/llm.py 双后端、数据可复原（CONSTITUTION §4） |
| 10 | 预算 | **分阶段审批**：冒烟 ≤$50；主实验前交预算估算文档批准后再跑；脚本必须带 `--max-cost-usd` 熔断 | |
| 11 | 文档语言 | **中文为主**；代码注释与论文英文 | |
| 12 | 规则强度 | **严格模式**：README + CHANGELOG + LEDGER 三件套是任务完成的一部分 | owner 不写代码，文档=全部可见性 |
