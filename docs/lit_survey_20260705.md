# 文献调研精华（2026-07-05）

> 6 个 research agent 核实原文后的结论汇总；原始结构化输出见 `lit_survey_20260705_raw.json`。写 related work / 回应"与 X 的区别"类审稿问题，以本文件为出发点，引用前用 `shared/fetch_bib.py` 里的 cite key。

## 1. 三篇 anchor 论文

### SkillOpt（Microsoft，arXiv:2605.23904，2026-05）→ cite key `skillopt2026`
- **是什么**：把单个 skill.md 当冻结 agent 的"可训练参数"。循环 = rollout 批（默认 40 任务）→ 失败/成功分组 minibatch reflection（每组 8，16 并行 worker）→ add/delete/replace 编辑 → "文本学习率"裁剪（每步 ≤4 条，cosine 衰减到 2）→ **held-out selection split 上严格提升才接受** → 被拒编辑进 rejected-edit buffer 反哺后续 reflection → epoch 级 slow/meta update 写入受保护区块。
- **结果**：6 benchmark × 7 模型 × 3 harness 全部 52 格最优或并列；GPT-5.5 direct chat 平均 58.8→82.3。
- **对我们最重要的限制**：只用 ground-truth verifier（明确不用 LLM judge）；纯 on-policy；单文档非库；任务必须自带 train/selection/test 划分；**严格-提升接受门在噪声 reward 下大概率失效**（REPLAY 模块 B 的直接切入点）。

### Training-Free GRPO（腾讯优图，arXiv:2510.08191，2025-10）→ `tfgrpo2025`
- **是什么**：冻结模型 + 经验库 E（"textual LoRA"）。同一任务采 G 个 rollout（math G=5 / web G=3），按 reward 分好坏后让 LLM 提炼"语义化组相对优势"，再产出对 E 的 Add/Delete/Modify/Keep 编辑。100 任务、3 epoch、约 $8-18 全程。
- **结果**：DeepSeek-V3.1-Terminus 上 AIME24 80.0→82.7、AIME25 67.9→73.3、WebWalkerQA 63.2→67.8；花 $18 打过 $10,000 训出来的 32B RL baseline。
- **对我们最重要的限制**：**需要同一任务重复采样产生组内 reward 方差**——一次性的真实用户交互没有这个结构；无 ground-truth 的 ablation 明显掉点（82.7→80.7 / 73.3→68.9）；纯 on-policy，无任何 off-policy 校正。
- 后续：Skills-Coach（arXiv:2604.27488）把它搬到 Anthropic 式 skill + 自动任务生成——**"TF-GRPO+合成数据优化skill"这个组合已被占**，REPLAY 的差异化必须押在真实日志上。

### Skill-RM（arXiv:2606.03980，2026-06）→ `skillrm2026`
- **是什么**：把 reward model 本身做成一个 SKILL.md 让 judge agent 执行（rubrics/参考答案/验证器/校准规则的资源库 + 结构化取证输出）。**全文没有优化环节，skill 是人手工策划后冻结的。**
- **定位**：不是竞品，是 motivation（其 limitation 原话：skill 的自动构建与持续自我改进是 open problem）+ 可以直接用作我们的 judge 组件。
- **有用的实验事实**：把同样的资源直接塞 prompt 反而 -2.9 分，skill 化编排 +2.3 分——"朴素堆知识进 context 会掉分"，支持我们做结构化条目管理。

## 2. 确认的文献空白（= REPLAY / WildLoop 的立足点）

方法侧 + 数据侧两轮扫描（38 篇）交叉确认，无人做到：

1. **真实离线日志作为 skill 优化数据源**：所有强优化器（SkillOpt/TF-GRPO/ACE/GEPA/SkillWeaver/Voyager/MIPRO）全是 on-policy 新鲜 rollout；离线派（ExpeL/AutoGuide/AWM/Memento）挖的也是 agent 自己带标签的轨迹，不是 messy 真实用户 session。【REPLAY 模块 A】
2. **off-policy 校正的文本类比**：日志由旧策略/别的 agent 产生，没有任何"文本空间的 importance weighting / 分布偏移校正"。【REPLAY 的 replay 探针】
3. **廉价有偏离线信号 × 昂贵无偏在线信号的融合**：两个文献群完全不相交。【REPLAY 主框架】
4. **judge-validity-aware 优化**：judge "reliable but not valid"（2606.19544）、可被 hack（2606.04923）、反馈优化滋生 manipulation（2411.02306），但没有 skill 优化器做 judge 校准/悲观门控/真实信号锚定。【REPLAY 模块 B】
5. **粗信号到条目的 credit assignment**：session 级噪声反馈 ↛ 库里哪一条该改。【REPLAY 模块 C】
6. **日志接地 simulator 的优化闭环 + 配套 benchmark**：RealUserSim（2605.20204）只接地不闭环；"真日志+可重放环境+双 reward"的 benchmark 不存在。【WildLoop 全部】

## 3. 关键引用弹药（写 intro/motivation 用）

- 隐式反馈可挖但噪声大、甚至 sign-flipped：`natfeedback2024`（~30% 对话含可提取反馈）、`noisyfeedback2025`（naive 用会掉点）、`implicitsentiment2025`（隐式信号覆盖率 ~13×于显式）、`rluf2025`（生产环境信号稀疏且 adversarial）
- judge 不可信：`judgereliability2026`（541k 判例审计）、`rewardhackingrubric2026`、`manipulation2024`
- simulator 不可信：`lostinsim2026`（simulator 选择可摆动 9pp）、`tau2bench2025`
- 逃出自我确认陷阱：`edv2026`（用多 agent 共识换外部验证——我们用真实日志信号替代，更便宜）
- 近邻方法定位：`ace2025`（单一 playbook、自产反馈）、`reasoningbank2025`（self-judged 合成轨迹）、`gepa2025`（要 task metric）

## 4. 投稿时间线（官方核实于 2026-07-05）

| venue | 截稿 | 可信度 |
|---|---|---|
| AAAI-27 | 摘要 2026-07-21 / 全文 07-28 | 官方确认（已放弃，太紧） |
| KDD 2027 cycle1 | 2026-07-26 | 官方确认 |
| EACL 2027 (ARR) | 2026-08-03 | 官方确认 |
| **ICLR 2027（主目标）** | **约 2026-09-16** | 历史规律估计，**官网发布后立即核实并更新此表** |
| ARR 十月 cycle（backup） | 2026-10-12 | 官方确认 |
