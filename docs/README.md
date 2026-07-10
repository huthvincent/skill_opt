# docs/ —— 跨论文文档

> 单篇论文自己的分析放各论文的 `Doc/`；只有两篇都相关的放这里。

| 文件 | 内容 |
|---|---|
| `judge_design_20260706.md` | **Self-evolve 裁判赛道设计（待 owner 决策打包方式）**：63 篇调研 → 七大缺陷（D1-D7）→ 六个改进方案（P1-P6）→ GATEKEEPER 合并设计（四层级联+元层）+ 抗攻性新指标 + 三种论文打包方式（推荐 A：裁判栈为主角） |
| `judge_survey_raw.json` | 上述设计的调研原始数据（4 agent × 63 篇：环内裁判/通用裁判/循环失效/工程产品） |
| `review_response_20260706.md` | **外部评审的逐条裁定（当前最重要）**：接受项（LCB bug 已修/设定矛盾/日志名不副实/统计纪律）、修正项（WISE-Flow 降级中威胁、GRASP 的统计门指控被驳回、G2=0.68 反转为领域天花板）、新颖性措辞、主实验预注册规则、**待 owner 三选一的设定重构** |
| `review_verification_raw.json` | 上述裁定的一手核实数据（4 个 research agent 对 WISE-Flow/GRASP/judge-AUROC/会议档期的原始输出） |
| `trans.md` | **跨机器交接文档**：给新 server 上 AI agent 的冷启动入口（项目速览、必读清单、搭建步骤、坑清单、资产清单、下一步 G0-G2） |
| `sanity_check.md` | **v2 验证计划（当前有效）**：G0 可控性→G1 单条目闭环→G2 信号→G3 对垒纯on-policy；前三门仅 ~$11。待充值后执行 |
| `pivot_proposal_20260705.md` | 转向提案（**已被 owner 否决**，2026-07-05）：owner 明确 motivation 不变（日志→优化 skill），要求重设计方法而非换问题。调研结论仍有价值（评估侧地形图 + 新引用） |
| `pivot_due_diligence_raw.json` | 上述尽职调查的原始输出（Eval-Skill 深读 + 裁判优化/路由两个地形扫描） |
| `method.md` | **通俗版方法完全讲解（v2，与 PROPOSAL v1 同步）**：九层由浅入深——skill 是什么→别人的盲区→日志 motivation→第一版失败教训→医生开药六步→为什么这次能 work→对比表→sanity check 四门→论文卖点 |
| `lit_survey_20260705.md` | 文献调研精华：三篇 anchor 论文的方法/限制、方法侧+数据侧 landscape、确认的 6+10 条空白、投稿时间线。**写 related work 先读这个** |
| `lit_survey_20260705_raw.json` | 调研的原始结构化输出（6 个 research agent 的完整结果），上面精华版的数据来源 |
| `decisions_20260705.md` | 12 项架构决策的完整记录（选项、答案、理由）——"为什么当初这么定"来这里查 |
