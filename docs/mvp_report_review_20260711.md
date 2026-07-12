# CAGE MVP 报告评审（本机 agent，2026-07-11）

> 对另一台 server 回传的 `outside_reports/final_report.md` 的独立评审。注意：只回传了 report，**原始产物（ledger.jsonl/curves.csv/archive/config.json）未传**，本评审基于 report 文本 + 内部一致性检查。

## 一、报告质量：高，诚实，数字自洽
- 内部一致性抽查通过：Phase 2 空库基线 0.700 = (40×0.725 + 20×0.65)/60 ✓，说明报告非杜撰。
- 三阶段递进（主实验→能否逼 DP>1→能否提升真值），结论口径克制（只陈述事实），踩坑如实记录（tau2 全局目录 EOF、CI 逐组件化修复）。
- 花费 $713/硬帽 $1500，未触帽。

## 二、结果三层
1. 主实验：三臂 DP 均未过 1（CAGE 峰 0.44）；但 CAGE 有干净方向性优势（判对率稳、背离 −0.225→−0.025 收窄）；Static 不收敛、CoEvo 精度漂移。
2. Phase 1：穷尽 rubric/few-shot/L0 探针/换 Opus，diverse held-out 上 DP 最高 0.34。诊断：**信息缺口**——文本裁判判不出散文式 forge 背后有无落库。
3. Phase 2（最关键）：8 库×3 种子，真值测量。**无一显著超空库**（CAGE_full +1.1pp, p=1.0），多数降，CAGE_real_only −11.1pp。→ 会被骗的裁判筛出的库对真值无正贡献。

## 三、负结论成立，但"接受"下早了——三个便宜可测、均未测的替代解释
1. **Haiku 天花板（最关键，报告自认未执行）**：Phase 2 用 Haiku 做题家。"库没用" vs "Haiku 听不懂好建议"未分离。Sonnet-agent 复跑已预批但选 C 未做。~$15 实验，不做则负结论悬空。**这是自 Gate 1 起就一直没干净排除的同一个 G0 可控性问题。**
2. **forge 攻击不现实拉低 DP**：archive 66% 是 `forge_tool_result`（篡改工具返回）。真实优化中 agent 拿真返回、无法篡改工具结果，realistic 攻击只有另外 34%（unbacked_claim/verbose_sycophancy/format_masquerade）。用 forge 算 DP 使裁判显得比现实威胁更易骗；只算 realistic 攻击 DP 可能显著更高。
3. **tau2 自由文本废掉 L0**：确定性探针"宣称成功但无对应成功工具调用"因 tau2 user-sim 自由文本而误伤真成功。换 AppWorld（结构化 API+真返回）L0 应干净得多——AppWorld 本就是规划的第二 benchmark。

## 四、战略重定位（核心）
CAGE 作为**方法**拿负结果，但作为**测量仪器**恰好干净实证了领域第一大空白（见 `field_direction_20260706.md`）：
- Phase 1 = 进化信号不可信（judge 证不出真伪）；
- Phase 2 = 进化态对真值无益（"memory in a costume"）。
→ 从"提出 CAGE 解决 self-evolve"重定位为"用 CAGE 仪器证明 self-evolve 信号为何失败 + 认证需要什么"。负结果 + 机制诊断 + 认证判据 = 可发，且正中领域第一大空白。

## 五、建议的下一步（按性价比，全部便宜）
1. **先要原始产物**：让那边把 `output/`（ledger/curves/archive/config/phase1/phase2）打包传来，才能在此之上建论文（宪法：不在未核数据上下结论）。
2. **补 G0/Sonnet-agent 复跑**（~$15）：这是唯一能把"文本库真没用"与"Haiku 天花板"分开的实验，且报告已预批。不做，任何结论都不 solid。
3. **realistic-only DP 重算**（零成本，用已有 archive）：剔除 forge_tool_result，只用 agent 可执行攻击重算 DP，看是否接近 1。
4. **AppWorld 小复现**（若走认证仪器路线）：结构化环境验证 L0 确定性层是否救回信号。
5. 论文重定位决策交 owner：A) 修 CAGE 方法（补 2+3+4 看能否翻案）；B) 直接把"负结果+诊断+认证框架"写成"self-evolve 信号何时可信"的论文（正中领域空白）；C) 彻底接受负结论、转向。

## 六、与既往的一致性
Phase 2 的 CAGE_real_only −11.1pp 与最早 Gate 1（整库注入有害）、Skill-RM 消融（裸堆知识 −2.9）完全一致：**tau2-retail 上 Haiku agent 的文本经验库注入反复无正收益**。这条证据链现在有三次独立复现——要么是稳健的真实现象（则领域认证/negative 论文成立），要么是 Haiku 天花板的三次重复（则 §五.2 必须做）。二者之分，全系那个 ~$15 的 Sonnet 复跑。
