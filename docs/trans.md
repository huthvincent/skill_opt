# 交接文档 —— 给新 server 上的 AI Agent

> 你好。你正在接手一个进行中的论文项目。这份文档是你的**冷启动入口**：项目是什么、读哪些文件、踩过哪些坑、下一步做什么。写于 2026-07-05（原开发机 /data2/zhu11/skill_Opt，已完成 9 个 commit 并推送）。
> **读完本文档后，按 §2 的顺序读完必读文件再动手。**

---

## 1. 三分钟版：这个项目是什么

**一篇目标 ICLR-27（约 2026-09-16 截稿）的论文（代号 REPLAY）+ 一篇排队中的（WildLoop）。**

研究问题：**当我们拥有真实用户与 AI agent 的交互日志时，如何更好地优化 agent 的文本经验库（skill）？** 现有方法（SkillOpt、Training-Free GRPO、ACE）全都只会"现场做有标准答案的练习题"，用不上部署中最丰富的真实日志（off-policy、无标准答案、只有噪声隐式反馈）。

**方法核心（v1 重设计后）**："日志提出，门控裁决"——日志失败聚簇免费告诉我们该在哪买能力（省掉昂贵的 on-policy 探索），小预算定向 rollout 逐条验证候选经验条目（簇匹配小样本大效应 + 无害对照 + 置信下界准入），触发签名条件注入。卖点术语："日志提供验证经济学"。

**重要历史**：第一版方法（批量生成 12 条整库注入）已被 ~$18 的实验**证伪**（与 Skill-RM 消融、SkillOpt "1–4 条已验证编辑"的实证一致）——这段失败是故事的一部分，进论文 intro。当前一切以 **PROPOSAL v1 / sanity check v2 / method.md v2** 为准。

## 2. 必读文件（按此顺序，全在仓库里）

| 顺序 | 文件 | 为什么读 |
|---|---|---|
| 1 | `CONSTITUTION.md` | **项目宪法，硬性规则**：目录职责、run_id 规范、文档三件套义务、预算纪律、可移植性红线。你的所有行为受它约束 |
| 2 | `docs/method.md` | 方法的通俗完全版（九层由浅入深），含第一版失败的教训与机理 |
| 3 | `REPLAY/PROPOSAL.md` | 方法技术正典 v1（与代码冲突时以它为准） |
| 4 | `docs/sanity_check.md` | **你接下来要执行的计划**（v2：G0→G1→G2→G3 四道门） |
| 5 | `REPLAY/README.md` + `REPLAY/LEDGER.md` + `REPLAY/EXPERIMENTS.md` | 当前进度、每个 run 的台账（含 3 次失败 run 的教训）、实验登记表 |
| 6 | `shared/README.md` | 基础设施：llm.py 双后端、runharness、tau2_compat 三补丁 |
| 7 | `docs/lit_survey_20260705.md` | 文献坐标（写论文时用；日常实验可后置） |
| 8 | `REPLAY/Doc/budget_estimate.md` | 预算模型（单集 $0.094 实测锚点） |

## 3. 新机器搭建步骤（严格按顺序）

```bash
# ① clone 主仓库（私有库，需要 owner 的 GitHub 认证/SSH key）
git clone git@github.com:huthvincent/skill_opt.git skill_Opt && cd skill_Opt

# ② 先恢复 third_party（必须在 uv sync 之前！它是 uv workspace member，缺了 sync 直接失败）
cd third_party
git clone https://github.com/sierra-research/tau2-bench
cd tau2-bench && git checkout 1901a301961cbbe3fd11f3e84a2a376530c759e3 && cd ../..

# ③ uv 环境（没有 uv 就先装：curl -LsSf https://astral.sh/uv/install.sh | sh）
uv sync          # 自动拉 Python 3.12 + 全部依赖 + tau2 editable

# ④ 配置 API（.env 永不 commit，已在 .gitignore）
cp .env.example .env    # 填入新的 API key（见 §4 后端选择）

# ⑤ 三步验证（花费 <$0.01）
uv run python -m shared.llm --selftest              # LLM 通路
uv run python REPLAY/script/tau2_probe.py           # 零成本结构探测（应全绿）
cd REPLAY/latex && latexmk -pdf main.tex && cd ../.. # 可选：论文编译（需 TeX Live）
```

## 4. 后端选择（关键注意点）

`.env` 的 `LLM_BACKEND` 支持 `anthropic`（直连）/ `bedrock`（AWS）/ `mock`（零成本假回复，调试管线用）。

**⚠️ 若用 Bedrock，有一处已知的适配工作**：`shared/llm.py` 走 AnthropicBedrock 没问题，但 **tau2 内部走 litellm**，实验脚本里的模型串是直连格式（`anthropic/claude-haiku-4-5-20251001`）。Bedrock 下需要把脚本里的 `MODEL` 常量改成 litellm 的 bedrock 格式（形如 `bedrock/us.anthropic.claude-haiku-4-5-...`，具体 model id 以 AWS 控制台为准），并确保 AWS 凭证在环境里。若用新的直连 Anthropic key，**零改动**。

## 5. 踩过的坑（全部已解决，但你必须知道）

1. **永不修改 `third_party/` 上游代码**（宪法红线）。tau2 有两处 gpt-4.1 硬编码（NL 判卷模型、env interface）且无 CLI 开关——解法在 `shared/tau2_compat.py`：`apply_default_model_patches(MODEL)` 必须在 `import tau2.cli` **之前**调用（import 顺序敏感，函数内有断言保护）。经验库注入用同文件的 `set_policy_suffix()`。
2. **推理模型会输出空文本**：fable-5 类模型会把 max_tokens 全花在内部思考上。`shared/llm.py` 已改为空文本抛错 + 自动去 temperature 重试；给 optimizer 角色调用留足 max_tokens（≥8000）。
3. **噪声带 ±10pp**：n=60 的全集成功率重跑方差实测 ±10pp。**一切判定用配对比较和定向集大效应**，别看全集小差值（详见 method.md 第六层）。
4. **预算纪律**（宪法 §6）：分阶段审批制；每个实验脚本必须走 `shared/runharness.Run` + `CostTracker(max_cost_usd=...)` 熔断；**任何门红灯 → 立即停、报告 owner**，不许自行加码。上一个账户就是烧干的（教训：跑长实验前先看账户余额）。
5. **文档三件套是任务完成的一部分**（宪法 §5）：改动更新所在目录 README + 根 CHANGELOG 一行 + 实验登记 LEDGER。Owner 不看代码，只看文档。
6. `gate1_ceiling.py` 实现的是**已废弃的 v0 整库测试，不要照跑**——但它的 `tau2_run()`/`stats()`/断点续跑模式是好的代码参考。
7. tau2 每集耗时 ~1 分钟；长批量务必后台跑 + 并发 ≤6。tau2 的 NL 判卷调用不计入 agent_cost/user_cost（预算时留 ~10% 余量）。

## 6. 手里的资产（全在仓库内，直接用）

| 资产 | 位置 | 用途 |
|---|---|---|
| 干净基线：haiku 无库 retail-30 = **70%**（n=60） | `REPLAY/results/gate1_ceiling_20260705_185023/base_results.json` | 对照锚点 + **当作"日志"用** |
| 12 个已知失败任务 id（2,3,4,6,7,8,16,20,21,22,27,28） | 同上 run 的 metrics/LEDGER | **现成的失败簇**，G0/G1 直接用 |
| 12 条"天花板"经验库 | `REPLAY/results/gate1_ceiling_20260705_190509/library.md` | G1 候选条目的起点（逐条拆开验证） |
| ~170 条带隐藏 DB 真值的轨迹 | `REPLAY/results/*/{base,lib}_results.json` + `smoke_tau2_*/results.json` | **G2 的免费评测集**（judge AUC 对照真值） |

## 7. 你的下一步（按 sanity_check.md v2 执行）

**前置**：与 owner 确认新账户可用预算；G0–G2 合计约 $11。

1. **G0 可控性预门（~$2）**：写 `REPLAY/script/gate0_controllability.py`——取 3 个基线稳定失败任务（建议 3/6/7，基线 0%），强模型看着 `evaluation_criteria` 写"金条目"（允许作弊+任务专属），用 `set_policy_suffix` 单任务单条目注入，各 2 trial。**≥2/3 翻案 = 过**；不过 → 换 sonnet 当 agent 重测一次，再不过就停下报告。
2. **G1 单条目闭环（~$5）**：走通 PROPOSAL v1 步骤 1–3 的最小版（详见 sanity_check.md G1 节）。**≥1 个变体通过准入门 = 方法闭环成立**。
3. **G2 信号质量（~$4）**：用 §6 的 170 条轨迹测 judge+隐式信号的 AUC（≥0.75 过）。可与 G1 并行。
4. **三门跑完 → 停，向 owner 汇报三门结果**，获批后才进 G3（~$40）。
5. 每一步遵守：runharness 出 REPORT → LEDGER 登记 → CHANGELOG 一行 → commit（署名 `huthvincent <huthruiz@gmail.com>`，见仓库 git config）→ push。

## 8. 联络与边界

- 决策权在 owner（中文沟通）：预算超阶段、门红灯、方法变更、任何破坏性操作（force push / 删数据）都必须先问。
- 两台机器可能并行开发：**动手前先 `git pull`**，commit 频繁、消息规范（`[REPLAY|WildLoop|shared|docs] 一句话`），避免大分叉。
- 原机器上的会话记忆不会同步给你——**仓库文档就是全部事实来源**；你发现文档与实际不符时，修文档并在 CHANGELOG 记录。

祝顺利。三门全绿的话，这篇论文的核心主张就立住了。
