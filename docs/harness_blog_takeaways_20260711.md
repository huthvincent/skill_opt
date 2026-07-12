# Lilian Weng "Harness" 博客对本项目的启发（2026-07-11）

> 来源：https://lilianweng.github.io/posts/2026-07-04-harness/（2026-07-04，综述/position，非方法论文）。
> 价值：不提供新机制，但提供①项目升维框架 ②对我们诊断的顶级独立背书 ③一批可引用的命名概念 ④两个具体可落地的方法改进。

## 一、最重磅：它独立说出了我们 CAGE-v2 的核心设计原则
博客原话（关于自我改进的 reward hacking）：**"A self-improvement loop optimizes whatever signal it is given. If the reward comes from unit tests, the agent may overfit to tests; if it comes from a judge model, it may learn reward hacking tricks."**
→ 这**逐字**就是我们的诊断（裁判信号不可信是一等问题）。领域顶级研究者把它列为自我改进的**头号瓶颈**（"weak evaluators"）。

更关键的一句：**"The evaluator and permission control should likely sit outside the loop that evolves harness."**
→ 这**正是** CAGE-v2 的诚实性支点——gold verifier 只当"幕后冻结锚"、永不进准入循环。我们原以为这是个自创技巧，其实是 Lilian 独立提炼的设计原则。**这条从"我们的小聪明"升级为"有据可引的领域原则"，可以放到方法的正当性论证里。**

## 二、框架升维：从"skill 优化器"到"harness 工程"
博客把研究对象从"优化 context 内容"抬升到"优化 harness 本身"——harness = 编排层（工作流+评估+权限+持久状态）。
- **MCE（Meta Context Engineering）**：分离"机制（怎么管 context）"与"内容（context 里是什么）"，双层优化——内环给定 skill 找最佳 context，外环进化 skill 本身。
- **Meta-Harness / Self-Harness**：被优化对象变成 harness 代码本身；Self-Harness 三段循环 = **弱点挖掘 → 有界提案 → 验证**。
- **STOP / ADAS / AFlow / AlphaEvolve / DGM**：一系列"优化编排代码"的工作。

**对我们的含义**：CAGE 目前定位是"经验库（context/skill）优化器"——这是拥挤的低维。**升维定位 = "为自我改进解决评估器瓶颈的 harness 组件：一个接地的、对抗共进化的、置于循环之外的评估器"。** 这个定位①正踩 Lilian 刚点名的头号瓶颈；②比"又一个 skill 优化器"高一档、更及时；③我们的红队+接地+gold-behind-glass 恰好是这个瓶颈的直接答案。

## 三、两个可直接落地的方法改进
1. **Provenance-at-write-time（比事后解析声称更稳）**：博客的 ScientistOne 用 **"Chain-of-Evidence checks：every claim (citation/numerical/methodological/conclusion) must trace to an evidence source and is audited"** + "file system as persistent auditable memory"。
   → 改进我们的接地裁判：不要事后去解析 agent 的散文声称（脆弱），而是**在写入时就强制每条声称引用支撑它的工具调用/DB 写入（写进可审计日志），准入时裁判审计这个引用链**。这正是 CAGE-v2 §六"溯源引用"的强化版，且现在有 ScientistOne 当出处。实验 0 的 J1 可以顺势升级为"审计声称-证据链"而非"解析散文"。
2. **双层形式化（给 CAGE-v2 一个干净的数学骨架 + 引用）**：用 MCE 的 bi-level 表述 CAGE-v2——**内环**：给定当前接地裁判，优化经验库内容；**外环**：针对冻结锚进化裁判机制（接地探针集），红队提供对抗性弱点挖掘。→ 把"共进化"从比喻变成 well-posed 的双层优化，且可引 MCE。

## 四、可引用的命名概念（related work / motivation 弹药）
- **"numerical duct tape and declare victory when signals are still noise"**（Trehan & Chopra 2026）= 我们的 fabrication/false-success 类的**领域命名**。强力 motivation 引用，直接对应 unbacked_claim 攻击。
- **Self-Harness "weakness mining → bounded proposal → validation"**：与我们 G 回合（失败聚类→候选提案→统计门）几乎同构，且其弱点挖掘是 **"verifier-grounded patterns"**——**再次印证"接地"是对的**。可定位 CAGE-v2 = "把 Self-Harness 循环用到裁判自身，弱点挖掘由红队对抗提供"。
- **"Held-out tests, trace audits, and human review at decision points"** = 我们的锚集 + 轨迹接地探针 + 统计门的对应。
- **DGM 自改写会移除自己的幻觉标记** = "evaluator 必须在循环外"的反面教材（与我们领域空白分析里的记录一致）。
- 负结果代表性不足 / "模型不擅长放弃失败假设" → 支撑我们 hindsight-relabel（失败→"不要编造"负例）。
- 多样性坍缩（diversity collapse）→ 支撑 CAGE-v2 的 QD best-per-bin 保留。

## 五、行动项（不改变实验 0 的生死判定，只优化定位与措辞）
1. **实验 0 的 J1 可选升级**：从"解析散文声称"改为"审计声称→工具调用/DB 写入的证据链"（Chain-of-Evidence 式），更稳、更可引；生死判据不变。
2. **CAGE-v2 定位升级**：写作/汇报时锚定"harness 工程解决评估器瓶颈"，而非"skill 优化"；把"evaluator outside the loop"作为核心设计原则显式论证（引 Lilian）。
3. **形式化**：用 MCE 双层框架写 CAGE-v2 的方法节。
4. 新增引用入 refs：Lilian harness 综述、MCE、Self-Harness、ScientistOne、Trehan&Chopra 2026、ADAS、AFlow、STOP、AlphaEvolve、DGM（精确 arXiv 号待补，本文只记概念映射）。

## 六、诚实边界
博客是综述/position，**不提供解决我们接地问题的新机制**——claim-derived 接地探针仍是我们自己的贡献，实验 0 仍是它的生死判定。博客的价值是**框架、背书、命名、两处方法强化**，不是免掉我们的核心实验。
