# 外部评审回应与裁定（2026-07-06）

> 背景：owner 在另一台 server 跑了部分 sanity check（结果 docx 在 owner 本地），并请一个独立 AI agent 评审。本文档是本机 agent 对该评审的**逐条独立核实与裁定**（4 个 research agent 从一手来源验证），以及由此产生的行动清单与待 owner 决策项。
> 原始核实数据：`review_verification_raw.json`（同目录）。
> ⚠️ 前提缺陷：另一台 server 的 pilot 数据/脚本**尚未 push**，本文引用的 pilot 数字（G2 AUC=0.68、0/3→3/3 等）均转引自评审文本，待那边入库后核对。

---

## 一、对评审各发现的裁定

### 1.1 接受（评审正确，必须修）

| 发现 | 裁定 | 状态 |
|---|---|---|
| **LCB 是 Wald 伪影**（0/3→3/3 报 "+100pp"） | ✅ 完全成立。正确计算：Agresti-Caffo 95% 单侧 LCB = **+18.4pp**（本机已复算） | **已修**：`shared/stats.py` 提供 Clopper-Pearson / Agresti-Caffo / 配对 bootstrap，附"n<8 时 bootstrap 退化"警告。另一台机器的 gate 脚本必须改用此模块并重算全部已报数字 |
| **设定与方法自相矛盾**（立论"无标准答案不可重跑"，验证却靠可重放环境+隐藏判分器） | ✅ 完全成立，是最深的地基问题 | 待 owner 三选一（见 §三） |
| **"真实日志"名不副实**（同分布、同任务池、实为 on-policy 合成） | ✅ 成立 | 修法已定（不需 owner 决策）：①措辞全面改为 "simulated deployment logs"；②日志生成改用**旧模型+旧 prompt+不同任务子集**制造真 off-policy；③WildChat 真日志副线升级为必做（这是所有竞品都没有的证据） |
| **G3 证据不足**（n=1 簇、单 seed、修 bug 后重跑、成本记账有利于己方） | ✅ 成立。pilot 只证明"管线能跑通" | 主实验按 §四 的预注册设计重做；内部措辞全部降调（"机制被证明有效"→"管线冒烟通过"） |
| **Winner's curse / 开发-评测泄漏 / rerun-until-green** | ✅ 成立 | 写入主实验设计规则（§四）：discovery/confirmation 分批、预注册冻结、held-out 簇评测 |
| 时间线：放弃 AAAI-27，主攻 ICLR 2027，备胎 ICML 2027 | ✅ 官方来源核实无误：ICLR 2027 未发布（iclr.cc 404），按 2026 规律估摸要 9-19/9-24；AAAI-27 Phase-1 拒稿通知 9-24 与 ICLR 截稿冲突；ICML 2027 约 1 月底 | 采纳。8 月起每周盯 iclr.cc（只信 iclr.cc 与 OpenReview，已有假会议条目在流传） |

### 1.2 修正（评审有误或夸大，经一手核实）

| 评审判断 | 核实结果 |
|---|---|
| **WISE-Flow（2601.08158）威胁"高"** | **降为中**。确认存在、确认 τ²-bench、确认"日志→文本经验、training-free"。但逐点比对：**无失败聚类**（用的是 outcome 分类+对比对）、**无任何逐条实证验证**（只有 LLM 对着源轨迹自我反思）、**无统计门、无无害对照**（其 limitation 自认有害注入是未解决风险）、**无经济学主张**、其"日志"同为模拟器自采 rollout。定位：**必引 + 必列 baseline**，但没占死我们任何核心机制 |
| **GRASP（2605.29668）"与六步法几乎同构、悲观准入门被占死"** | **前半部分成立、后半 REFUTED**。确认存在且重叠度高：有失败聚类（LLM 分类器→机制级标签）、有逐簇候选（K=4 ADD/MODIFY/REMOVE）、有 held-out probe + 回归预算门——"带验证的库编辑"这个范式确实被它推向主流。**但它的门是原始计数算术**（F−R>0 且 R≤R₀），**无置信界、无假设检验、无悲观性**；probe 是全局平衡集**而非簇匹配定向集**；数据**完全 on-policy dev-split，从不碰日志**；无预算对垒实验。→ "统计悲观准入门"这个贡献**不必让给它**，但必须与它正面对比并把差异写得极其精确 |
| **G2 的 0.68 是软肋** | **可反转为设计动机，但引用要改**：正确的引用是 **arXiv:2606.09863**（就在 τ²-bench 上：5 judge 模型×5 prompt×3 表述、甚至喂全量任务说明，最强配置 AUROC < 0.65，推理模型更差 0.573/0.554）；评审给的 2606.10315 是生产环境餐饮 agent 的 recall 证据（内置 judge 操作性召回 0%），可作辅证。我们的 0.68 **等于或高于该 benchmark 的领域天花板** → 写成"judge 单层不可依赖是领域公认事实，因此必须弱裁判粗筛+真验证兜底的双层架构" |

## 二、修订后的新颖性定位（措辞级，写进论文前逐字核对）

**禁写**："first to optimize skills from real interaction logs"（WISE-Flow/AutoGuide/O3D 足以拒稿）。

**可守的组合**（每条都经一手核实无人占有）：
1. **Off-policy 日志复用作为核心机制**：GRASP 全程 on-policy 不碰日志；WISE-Flow 的日志是无验证的自采 rollout。加上真 off-policy 构造（旧模型旧 prompt）+ WildChat 真日志，这条能守住；
2. **簇匹配定向验证 + 统计悲观准入门**：GRASP=全局 probe+原始计数；WISE-Flow=自我反思。"小 n 大效应的定向配对验证 + LCB 准入"无人做；
3. **验证经济学的形式化 + 同预算 off-vs-on-policy 对垒**：两家皆无此主张与实验；
4. **裁判不可靠条件下的双层架构**（judge AUROC≤0.65 领域天花板为动机，弱裁判粗筛+真验证兜底+实测脏信号下的假准入率）。

⚠️ WISE-Flow(1月)→GRASP(5月) 只隔 4 个月，方向正被快速填满：**主实验一完成立刻挂 arXiv 占位**。

## 三、设定重构：待 owner 三选一（评审与本机 agent 均倾向 b）

| 选项 | 内容 | 代价/收益 |
|---|---|---|
| (a) 诚实改设定 | "离线日志 + 一个带判分的 staging 环境"；把构造靶点任务的成本计入经济学账本 | 最便宜；但"staging 有判分器"仍偏乐观 |
| **(b) 裁判信号做验证**（推荐） | 准入门的验证信号换成 judge（AUC≈0.68 的脏信号），**实测悲观门的假准入率/漏准入率**，隐藏 verifier 只做终评标尺 | 这才是配得上设定的实验；把 G2 从软肋变成主实验；悲观门的价值有了直接证据（对比原始计数门/严格门在脏信号下的崩坏）——**与 GRASP 的差异化也由此坐实** |
| (c) 纯离线验证（OPE 类比） | 不重跑，用日志做 off-policy evaluation 式验证 | 学术上最激进但技术风险大、11 周窗口内不现实；可作 future work |
| 本机建议 | **(b) 为主 + (a) 的措辞框架**：设定=“simulated deployment logs + judge 可用、verifier 不可用”；(c) 写进 discussion | |

## 四、主实验设计规则（预注册冻结清单，跑前逐条打勾）

1. **统计单元 = 失败簇**：≥20–30 个独立簇，跨 τ²-bench retail + airline + WildChat 真日志设定；
2. **discovery / confirmation 分批**：选候选与过门用 discovery 批；效应量只在 confirmation 批上报告（否则 winner's curse）；
3. 每靶点 ≥10 seed；簇级配对检验 + bootstrap CI（用 `shared/stats.py`）；
4. **held-out 簇**：pilot 碰过的任务（2/3/4/6/7 等）只进 discovery，永不进终评；
5. baseline：WISE-Flow、GRASP 式（全局 probe+计数门）、ACE 式、SkillOpt 式、无优化、oracle 上界；
6. 消融必含：−悲观门（换原始计数门）、裁判质量扫描（verifier→强judge→弱judge 的准入质量曲线）；
7. 预算：全功效 $3–5k；若锁 $2k，**砍域不砍 confirmation 批**（宁窄勿虚）；成本按 episode 数报告，美元仅附注；
8. 模型版本号钉死写入 config.json（已有）；脚本与 transcript 随投稿开源。

## 五、行动清单

**本机（已完成）**：`shared/stats.py`（LCB 修复+自检）✅；竞品一手核实 ✅；本文档 ✅；refs.bib 增补 4 篇（wiseflow/grasp/judge-auroc×2）✅。
**另一台 server（待办，按序）**：① **立即 commit+push pilot 全部产物**（宪法义务，两边事实基础已分叉）；② gate 脚本改用 `shared.stats`，重算全部已报数字并更新 LEDGER；③ 日志生成改旧模型+旧 prompt 造真 off-policy；④ WildChat 管线启动。
**Owner（待决策）**：① 设定重构三选一（§三）；② 主实验预算档位（$2k 窄域 vs $3–5k 全功效）；③ 是否采纳"9 月中挂 arXiv 占位"的节奏。

## 六、时间线（官方核实版）

| 节点 | 日期 | 状态 |
|---|---|---|
| AAAI-27 | 放弃（Phase-1 拒稿通知 9-24 与 ICLR 撞车，官方核实） | 定案 |
| Phase B / WildChat 管线 | 7 月中前 | 待跑 |
| 预注册冻结 + 主实验 | 8 月 | 待 owner 批预算 |
| arXiv 占位 + ICLR 2027 投稿 | 9 月中（截稿估 9-19/9-24，**以 iclr.cc 官方发布为准，尚未公布**） | 8 月起每周盯 |
| 备胎 | ICML 2027（约 1 月底） | |
