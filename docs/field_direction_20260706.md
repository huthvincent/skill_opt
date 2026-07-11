# Self-Evolving Agent 领域最大空白：深耕方向分析（2026-07-06）

> 问题：想在 self-evolving AI agent 领域深耕，最大的结构性空白是什么？做什么贡献最大、最有用？
> 方法：5-agent 调研（survey 自认空白 / 方法侧死结 / 评估侧缺口 / 落地安全侧缺口 + 高强度评判层交叉排序），28 篇 landmark（含 6 篇 2025-26 权威 survey + Microsoft position paper）。原始数据 `field_direction_raw.json`。
> **一句话结论：领域最缺的不是"怎么让 agent 变更好"，而是"怎么证明驱动它变好的信号本身没坏"——而这正是 CAGE 的加深，不是推倒。**

---

## 一、评判层的最终推荐（单一答案）

**深耕方向 = 自我进化信号的纵向认证（Longitudinal Certification of the Improvement Signal）。**

核心问题：*当 agent 不断进化时，驱动它自我改进的那个 judge/reward/verifier 信号，会不会在某一刻被 agent 悄悄"捕获"（gaming）而与真实目标脱钩？如何在脱钩发生的那一刻之前把它检测出来、并给出可证明的"这一步进化可信"的许可判据？*

三个理由让它成为**唯一诚实的答案**：

1. **复现性最强 = 领域共识**：它是**唯一在四个视角里独立浮现**的空白（survey 侧、方法侧、评估侧、落地侧全部指向它）。而且它**因果上游于几乎所有其他空白**——reward hacking、模型崩溃、安全漂移、"memory in a costume"全都是"信号不可信"的下游症状。
2. **与 CAGE 直接同源**：CAGE 已经在做 training-free 的 agent-judge 对抗共进化 + 认证终点 + 欺骗溢价。这个方向**只是把证书从"单个终点"抬升到"整条进化轨迹"**，问"这个证书在 t 步之后还成立吗"。你保留全部对抗-裁判机器和认证视角，只加两样东西：**anytime-valid 序贯统计** + **环外元验证器（out-of-loop meta-verifier）**。
3. **可攻克 × 有空白**：单个课题组用可验证域测试台（SWE-bench/math，有真值可校准元验证器）+ API 模型就能做，**不需要工业界规模训练**。2026 年开始有零星"meta-evaluation / calibration-as-reward"论文，但**对抗性欺骗溢价 + 认证终点的框架仍是空白，且正是你的差异化**。

**统一身份**：*"为自我进化 agent 提供可认证、抗崩溃的改进信号"（certified, collapse-resistant improvement signals for self-evolving agents）*——一个从 CAGE 长出来、且占住一个基础性且尚未拥挤问题的多年身份。

## 二、排序前五（含可攻克性与拥挤度诚实评估）

| 名次 | 空白 | 与 CAGE 关系 | 可攻克性 | 拥挤度 |
|---|---|---|---|---|
| **1** | **进化信号的纵向认证**（判据+理论+仪器，检测 optimizer-optimizee collapse） | **直接加深** | 高（可验证域+API+序贯统计，无需大训练） | 低-新兴 |
| **2** | **污染防火墙 / 过程级测量**（自改写 agent 的"改进 vs 平台期 vs 崩溃"无操作性定义；held-out 一被 agent 流经就失效） | **协同**（做 gap1 认证主张可证伪的评估底座） | 最高（方法/benchmark/基建，最省算力） | 表面中/真防火墙低 |
| 3 | **进化不变的安全内核**（agent 无限次自编辑仍保持固定安全不变量，而安全监视器本身在优化范围内） | 半延伸半转向（偏形式化/系统） | 部分（受限编辑类可做，完全保证不可） | 低但快速上升 |
| 4 | **非退化自我提升的理论 + 在线崩溃预警**（自训练的 rise-and-collapse 相变边界；在能力已损失前预警） | 相邻转向（共享环外认证哲学，研究动力学非对抗） | 高（崩溃可在小规模复现，预警器是具体产物） | 中/升温 |
| 5 | **长程多会话 credit assignment + 溯源**（几千次记忆写入后无法归因某次结果到具体经验） | 转向（机器全新） | 记忆归因版可做/完全 lifelong 不可 | RL 版拥挤/记忆溯源版较空 |

**关键洞察（评判层原话）**：gap 1 是承重墙，gap 2 是让 gap 1 可证伪的评估底座，gap 3/gap 4 是复用"环外认证器"哲学的相邻第二战线。**四者可以是同一个研究纲领的不同面，而不是四个孤立选择**——这就是"深耕"而非"打一枪换一个地方"的含义。

## 三、明确要避开的（当红但低产/拥挤，评判层点名）

1. **又一个记忆架构 / skill 库检索方案**（A-Mem、Mem0、Memento、SKILL.md 变体）——四路分析一致判为饱和；"wipe-test"证明存储/检索不是瓶颈；数百篇争缩小的 delta。
2. **不带纵向-对抗-优化压力框架的通用 LLM-judge 可靠性研究**——静态设定文献已巨量；价值只在"agent 一边 gaming、judge 跨迭代如何变化"。
3. **又一个只打终点成功率的静态 benchmark**——2025-26 已 benchmark 过剩；除非你交付的是它们都缺的污染防火墙/过程级测量。
4. **增量 RLVR 权重更新 / 经典遗忘-持续学习适配器**（replay/EWC/LoRA 移植到 agent）——拥挤，且 RLVR 多半只在基座 frontier 内重加权、封顶。
5. **多智能体编排 / 群体共进化的炒作**——多样性崩溃与传染结果显示不稳，失败是涌现/集体的，小组难做出干净进展。
6. **单次自我反思 prompt 技巧**（Reflexion 后代）——被基座自评能力封顶，一次后即平台。
7. **宏大的递归自我提升 / 元认知宣言**——无可验证测试台则不可证伪且不安全；只能从"可认证信号"或"不可变不变量"这些能被仪器化的子问题进入。

## 四、纲领化的首篇论文（占位 + 生根）

评判层给的具体首篇（都可落地、可 fund）：
- **主纲领（gap1）**：*"Does the Certificate Survive Iteration? Meta-Verification of Self-Evolving Agents."* 在可验证域上搭共进化测试台，让 agent 对着学习型 judge 进化，把欺骗溢价（judge 分 − 真值）画成迭代函数、实证展示 optimizer-optimizee collapse；引入环外、周期性刷新的独立认证器 + anytime-valid 序贯判据，在信号脱钩前触发。**——这就是 CAGE 从"单篇"升级为"纲领"的那一步。**
- **评估底座（gap2）**：*"A Contamination Firewall for Self-Modifying Agents."* 形式化"agent 本可吸收的信息"，做出第一个可证明在 agent 写/读历史之外、每 checkpoint 新鲜生成的 held-out 生成器 + 标准化 wipe-test-plus-regeneration + 随机改进零假设基线；在 2-3 个现有 self-evolve 方法上证明大部分"提升"是污染。
- 第二战线（gap4）：*"Predicting Rise-and-Collapse Before It Happens."* 崩溃相变边界 + 环外早期预警统计量。

## 五、对本项目的含义

- **CAGE 不是终点，是纲领的第一块基石**。当前 MVP（单终点认证）→ 纲领第一篇（全轨迹认证）→ 评估底座（污染防火墙）→ 第二战线（崩溃预警 / 安全不变量）。四步共享同一"环外认证器"哲学。
- **REPLAY/WildLoop 的资产全部沿用**：隐藏 verifier 协议、`shared/stats.py`（升级为 anytime-valid 序贯检验）、170 条带真值轨迹、tau2+AppWorld 测试台。
- **身份定位**：从"做 skill 优化的人"升级为"做**可信自我进化**的人"——一个更基础、更防拥挤、更有长期价值的学术身份。

## 附：本次调研核心 landmark（进 refs / 后续精读）
自我进化 survey 2507.21046 / 2508.07407；lifelong agent roadmap 2501.07278（TPAMI）；agentic RL landscape 2509.02547；self-improvement overview 2603.25681（含 misevolution/自纠盲点分类）；安全 survey 2606.23075（optimizer-optimizee collapse、Lamarckian propagation）；Microsoft position paper（verifier boundary、meta-evaluation 缺失）；崩溃 2606.21090 / misevolution 2509.26354；anytime-valid 2607.00871；memory 归因 2606.04990。精确清单见 raw。
