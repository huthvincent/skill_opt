# CAGE 的 Benchmark 选择（2026-07-06）

> 问题：tau2 是否最合适？同类文章都用什么？基于 4 个 research agent 一手核实（judge/reward-hacking/self-evolve/agentic 四路，原始数据 `benchmark_choice_raw.json`）。

## 一、CAGE 对 benchmark 的四条硬要求

1. 多轮工具调用轨迹（不能单轮问答，否则无"假成功"伪造空间）；
2. **隐藏的程序化真值**（确定性 DB-state/单元测试判分器，独立于任何 LLM judge）——锚/金丝雀/C1/C3 的命根；
3. 丰富的"假成功"攻击面（agent 声称成功但实际没做到，且难判）；
4. 任务量够做 54/40/20 三池划分（约需 ≥114/域）。

**第 2 条是最稀缺的过滤器**——它一次淘汰掉全部 judge 标准 benchmark（RewardBench/JudgeBench/RM-Bench 都是单轮问答、无程序化真值）和大部分 agent-eval 数据集（AgentRewardBench/Claw-Eval/AgentProcessBench 的真值是人工标注、非可重放环境）。

## 二、结论：tau2 是正确的主选，但要加 AppWorld 作第二 benchmark

**四路调研罕见地完全一致**：只有 **tau2-bench、AppWorld、WebArena** 三个同时满足四条要求——而它们恰好正是"假成功"权威研究（2606.09863）用的三个环境，因为每个都"多轮轨迹 + 确定性判分器 + agent 能对它撒谎"。

### tau2 作主选——被一手证据强力背书
- 多轮工具调用 ✅；DB-state 确定性判分器 = 干净的带外真值 ✅；
- **假成功攻击面有实测数据背书**：2606.09863 测了 9,876 条 tau2 轨迹，单控域 **45–48% 的失败是"假成功"**（agent 断言完成，DB 状态不符），且 **LLM judge 判别 AUROC 从不超过 0.65**——这正是 CAGE 要攻的面，而且已被论文量化，直接进我们 intro；
- 攻击"落在 judge 上而非篡改真值"（narrate success without the DB write），对共进化研究是**理想**形态：对抗压力打在裁判、真值岿然不动。

### ⚠️ 一个必须现在就修的划分问题
tau2 各域任务数：**retail 114、telecom 114、airline 仅 50、banking 97**。我们的 54/40/20=114 划分：
- **retail（114）和 telecom（114）正好够** → 三池划分建在这两个域；
- **airline（50）太小** → 降级为 OOD/eval-only 域，**不做三池划分**；
- （MVP 只用 retail 单域，此问题不影响 MVP；正式实验才涉及。）

**→ 需要同步修 MVP 指令与 PROPOSAL**：正式实验的域从"retail+airline"改为"**retail+telecom**（airline 仅作 OOD 泛化测试）"。

### AppWorld 作第二 benchmark——三条理由
1. **验证哲学同构、模态正交**：code-as-action agent 跨 457 API/9 app（均 42.5 次 API 调用/任务），**隐藏单元测试 + 附带损害检查**（还查"有没有造成预期外的副作用"）——候选里最丰富的程序化假成功面；2606.09863 实测 AppWorld 上 **75.8% 的失败是假成功、judge AUROC 仅 0.54（≈瞎猜）**；
2. **它是 training-free 自改进论文的事实标准**（ACE、Training-Free GRPO 都用它）→ **baseline 直接可移植、审稿人预期看到它**；
3. 750 任务 + 现成划分（105/60/168/417），三池划分绰绰有余，且 2026 年仍活跃维护。

WebArena 是天然的第三域（agent-memory 线 AWM/ReasoningBank 的事实标准），但部分任务用模糊匹配、真值不如前两者干净——**列为可选第三域，不进 MVP**。

## 三、同类文章都用什么（速查，供 related work / baseline 对齐）

| 论文类别 | 事实标准 benchmark |
|---|---|
| judge/reward-model（RewardBench 等） | 单轮问答，**不满足我们要求**（无工具轨迹）——只能作外部 judge 测试集，不作训练环境 |
| self-evolve/skill 优化（ACE/TF-GRPO/SkillOpt） | **AppWorld、WebArena**、ALFWorld、SearchQA、SpreadsheetBench、tau2 |
| reward-hacking（agent 向） | tau2、**Reward Hacking Benchmark (2605.02964)**、ImpossibleBench、SWE-bench |
| 假成功/agent 轨迹 judge | **tau2 + AppWorld + WebArena**（2606.09863 三件套） |

**额外发现的强相关资源**（进 related work，可能作外部 judge 评测）：Reward Hacking Benchmark 2605.02964（多轮工具 reward hacking，6 类程序化 exploit 检测）、ImpossibleBench 2510.20270（任意"通过"即作弊，最干净的假成功锚）、EvilGenie 2511.21654（专门的作弊**检测器**评测 benchmark，最贴 CAGE 的裁判侧）。

## 四、行动项

1. **MVP 不变**（retail 单域已是最优起点，airline 问题不影响）；
2. **改 PROPOSAL 正式实验计划**：域改为 retail+telecom 做划分、airline 仅 OOD；正式实验加 AppWorld 作第二 benchmark（模态正交 + 审稿人预期 + baseline 可移植）；
3. 新增引用：2605.02964、2510.20270、2511.21654 + AppWorld（2407.18901）进 refs.bib。
