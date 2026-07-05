# WildLoop —— 方法构想（v0，未细化）

> 状态：构想阶段。REPLAY 冒烟通过后再细化成与 `REPLAY/PROPOSAL.md` 同等粒度的正典。文献依据见 `../docs/lit_survey_20260705.md` §2 第 6 条。

## 一段话摘要

现有 skill 优化全部对着 vanilla user simulator 做 on-policy rollout，而 simulator 是不可靠代理（simulator 选择可使成功率摆动 9pp，Lost in Simulation, arXiv:2601.17087）；RealUserSim（arXiv:2605.20204）用真实日志给 simulator 接地但只用于评估、不闭环。WildLoop 做完整闭环：真实日志 → 挖掘行为画像接地 simulator → 在接地 simulator 上优化经验库（复用 REPLAY 优化器）→ **在 held-out 真实日志上验证**优化是否真的迁移，并量化"vanilla simulator 上优化 = 过拟合 simulator 伪影"的程度。配套发布 WildLoop-Bench：真实日志 + 可重放接地环境 + AI-judge/隐藏 verifier 双 reward 的评测协议——文献确认此类 benchmark 不存在。

## 预期贡献

1. 首个"日志接地 simulator 上优化、真实日志上验证"的闭环协议，量化 simulator 过拟合（新发现）；
2. 接地方法本身（行为画像抽取 + 失败诱发模式注入）；
3. WildLoop-Bench 资源贡献（可考虑 KDD/WWW resource track 双线）。

## 依赖与前置

- 复用 REPLAY：优化器全套、judge 封装、日志 schema、τ²-bench 接入。
- 新增：WildChat 画像挖掘管线；simulator 接地层（τ²-bench user simulator 的 persona/行为注入接口，冒烟时确认其可注入性——**这是本篇最大的技术风险，REPLAY E0.2 阶段顺手验证**）。
