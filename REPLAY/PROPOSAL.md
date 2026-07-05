# REPLAY —— 方法设计正典

> **本文件是方法的唯一正典**：代码与本文件冲突时以本文件为准并修代码；方法变更必须先改这里（CONSTITUTION §5.4）。
> 论文题目（工作版）：*REPLAY: Textual Experience Replay for Training-Free Skill Optimization from Real Interaction Logs*
> 目标 venue：ICLR-27（约 2026-09-16）。文献坐标见 `../docs/lit_survey_20260705.md`。

## 0. 一段话摘要

现有 training-free skill/经验库优化器（SkillOpt、Training-Free GRPO、ACE、GEPA）全部依赖当前策略新鲜合成的 on-policy rollout 和可验证 reward。但现实部署里最丰富的数据是**真实用户交互日志**：off-policy（由旧策略/别的 agent 产生）、只有噪声的隐式反馈和 AI-judge 近似、一次性不可重放。REPLAY 把 RL 的 experience replay 思想移植到文本空间：**日志负责提出**（高召回、便宜），**定向 on-policy rollout 负责裁决**（高精度、昂贵），中间由 replay 探针做分布偏移加权、由噪声校准的悲观门控防 judge-hacking、由条目级 counterfactual 归因决定改库里的哪一条。

## 1. 问题设定

- 冻结的 agent 策略 π(y|q, E)，E = 经验库（若干条 1-3 句的自然语言条目，注入 system prompt）。
- 可用数据两种：
  - **离线日志 D_log**：真实用户 × 旧 agent 的完整 session。无 ground-truth reward；只有 (a) AI judge 打分，(b) 隐式信号（用户改写、追问极性、任务放弃、最终采纳）。off-policy、不可重放、量大。
  - **在线环境 env**：τ²-bench 式，可用 user simulator 做 on-policy rollout，有隐藏 verifier（**优化器不可见**，仅评估用）。rollout 昂贵，预算 B 有限。
- 目标：在 rollout 预算 B 约束下最大化优化后 E 在真实分布上的任务成功率。

## 2. 方法：三个模块

### 模块 A：离线提案（offline proposal）
1. 对每条日志 session，用 judge + 隐式信号提取器估计结果分 r̂ 与失败描述；
2. 失败 session 聚类成失败模式簇（embedding 聚类 + LLM 命名）；
3. 每簇由 optimizer 模型对照当前 E 提出 ≤k 条**候选**经验条目（含"该条目声称能修复的失败模式"元数据）。
**立场：日志产出的编辑永远只是假设，绝不直接入库。**

### 模块 A'：replay 探针加权（off-policy 校正的文本类比）
对支撑某候选条目的每条日志证据，把当前 agent（带当前 E）放回该日志的决策点重放一步：
- 当前策略会做出与日志相同的动作 → 该失败对当前策略仍然成立，证据权重高；
- 已经不会犯这个错 → 证据过时，降权/丢弃。
簇的加权证据分决定其候选条目进入验证队列的优先级。这是"importance weighting"的文本类比，也是论文方法论上最独特的部件。**[待验证：探针一步重放的判定稳定性]**

### 模块 B：定向在线验证 + 悲观门控（on-policy adjudication）
1. 每条候选条目，在与其失败簇匹配的环境任务上跑**成对对照组**：G 组 {带候选 E∪{e} vs 不带 E}，同 seed/同任务——组的构造是 counterfactual A/B，不是 TF-GRPO 的同题重采样（这正是它无法消费一次性日志的原因，我们绕开了）；
2. 接受判据（**悲观门控**，替换 SkillOpt 在噪声下会失效的严格-提升门）：多 judge 集成（含 prompt 扰动）打分的**置信下界**提升 > 0 才接受；
3. 双信号一致性约束：接受还要求该条目不降低"日志隐式信号 replay 代理分"（防优化出只讨好 judge 的条目）；
4. 验证预算分配：候选按 (证据权重 × 日志信号与 judge 信号的分歧度) 排序——分歧越大越值得花 rollout 查清（RLTHF 的"买标签"思想移植为"买 rollout"）。

### 模块 C：条目级 counterfactual 归因（entry-level credit）
- agent 被要求在轨迹中引用用到的条目 ID（激活日志）；
- 长期维护每条目的统计：激活率、带/不带 win-rate（来自模块 B 的对照数据，免费副产品）、共激活对；
- 周期性生命周期操作：低 win-rate 条目退役、高共激活对合并、过宽条目分裂——每次操作同样过模块 B 门控。

## 3. 实验协议

### 3.1 主线：τ²-bench（可测量的"伪真实日志"协议）
关键设计：**用弱旧 agent（不同模型、无经验库、不同 prompt）× 多 persona simulator 批量生成"历史日志"，并对优化器隐藏 verifier 结果**——优化器只能看 judge 分和隐式信号，但评估侧有隐藏 ground truth，可以精确度量每个模块贡献与 judge-hacking 程度。
- 环境：τ²-bench retail / airline / telecom；指标 pass^k。
- **核心对比表（同等 rollout 预算 B）**：
  | 方法 | 数据源 |
  |---|---|
  | 无经验库 baseline | — |
  | TF-GRPO（judge 当 reward） | 纯 on-policy |
  | ExpeL / AutoGuide 式离线蒸馏 | 纯日志 |
  | ACE | 纯 on-policy |
  | SkillOpt 改造版（经验库化） | 纯 on-policy |
  | **REPLAY** | 日志 + 定向 rollout |
- 预期主结论：同预算下 REPLAY 显著更优；预算-性能曲线上 REPLAY 用 1/3~1/2 预算达到纯 on-policy 方法的满预算性能。
- Ablation：去掉 replay 探针加权 / 悲观门控→严格门 / 分歧路由→随机路由 / 隐式信号锚 / 模块 C。
- 诊断实验（模块 B 的招牌图）：judge-only 优化时"judge 分涨幅 vs 隐藏 verifier 真实涨幅"的背离曲线，REPLAY 的双信号锚定应显著收窄背离。

### 3.2 副线：WildChat 真实日志
- 选 2-3 个高频域（如代码求助、写作润色），从 WildChat 挖失败簇 → 产出经验库 → held-out 真实日志上重放式评估（judge + 双盲 pairwise）。作用是真实性证据，不承担主结论。

### 3.3 预算与模型
- agent = claude-sonnet 级；optimizer = 最强档；judge = haiku 级多实例集成（便宜+异质）。全部经 `shared/llm.py`，每 run 带 `--max-cost-usd`。
- 阶段计划：冒烟（τ²-bench 单域 5 任务跑通全 pipeline，≤$50）→ 预算估算文档 → 主实验。

## 4. 贡献清单（论文 claim 草稿）

1. **新设定**：首个从真实（off-policy、噪声隐式反馈）交互日志优化文本经验库的框架，附可测量的"隐藏 verifier"实验协议；
2. **新方法**：replay 探针分布偏移加权 + 分歧路由的验证预算分配 + 噪声校准悲观门控 + 条目级 counterfactual 归因；
3. **新发现**：量化 judge-only skill 优化的 reward-hacking，并证明真实日志隐式信号锚定能收窄它。

## 5. 已知风险与对策

| 风险 | 对策 |
|---|---|
| 混合优于单源的增益不够大 | 兜底叙事：预算受限下的样本效率优势（曲线图）；极端预算 sweep 找增益最大区间 |
| replay 探针判定不稳定 | 冒烟阶段先单独测探针的 test-retest 一致性；不稳则降级为轨迹相似度加权 |
| τ²-bench 上 baseline 复现成本 | TF-GRPO/ExpeL 逻辑简单可自实现；ACE 用官方代码；SkillOpt 无代码则按论文自实现并注明 |
| Skills-Coach 等并发工作逼近 | 差异化死守"真实日志"设定；投稿前重扫 arXiv |

## 变更记录

- 2026-07-05：v0 初稿（来自 ideation 会话的 idea A+B+C 合并方案）。
