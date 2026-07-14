# REPLAY 实验台账

> 每个 run 一行，倒序追加。规则：跑完实验未登记 = 任务未完成（CONSTITUTION §5.3）。
> 格式：`run_id | 日期 | 对应实验ID | 一句话目的 | 关键指标 | 一句话结论 | 进论文?`

| run_id | 日期 | 实验 | 目的 | 关键指标 | 结论 | 进论文? |
|---|---|---|---|---|---|---|
| gate1_ceiling_20260714_105916 | 2026-07-14 | Gate1 | 用 Rui 同款模型（**claude-haiku-4.5**）在 Copilot 上跑 pilot（对齐旧 Anthropic 基线） | 后端=copilot/claude-haiku-4.5, 5题×1, A=0/5 C=0/5, **全 max_steps、零 action、0 错误** | ⚠️ **重要发现：Copilot 版 Claude 不能作 tau2 user simulator**。轨迹显示 user 角色拒绝扮顾客、自称"I'm Claude, an AI assistant by Anthropic"，与 agent 陷入礼貌死循环至耗尽步数（Copilot 服务层护栏注入所致）。故 Copilot-haiku **无法复现** Rui 的 Anthropic-haiku 基线(70%)；gpt-4o 无此问题。→ Copilot 跑 tau2 须用 gpt 系，且与 Anthropic-haiku 不可比 | 否（负结果，记教训） |
| gate1_ceiling_20260714_103726 | 2026-07-14 | Gate1 | Copilot 后端 Gate1 **管线/rate-limit 파일럿**（非正式判定，n=5） | 后端=copilot/gpt-4o, 5题×1, A=0/5 → 库16条($0) → C=1/5, **0 错误 0 rate-limit**, 全程 $0 | **基建验证 PASS**：三阶段管线在 Copilot（concurrency=2）跑通, 无余额/限速问题, flat-rate 计费=0 ✅。**判定不可读**（n=5, +20pp=单题翻转; gpt-4o≠旧 haiku 不可比）。可放心跑 30×2 正式 sweep | 否（基建） |
| copilot_probe_20260714_101723 | 2026-07-14 | E0.5 | Copilot 后端 tau2 阶段：Copilot 模型能否作 agent 跑通域 function-calling | github_copilot/gpt-4o, retail 1 题, reward=1.0, DB Match 100%, tool_calling_ok=True | **GO**：Copilot Chat API 支持 tau2 域工具 function-calling 并返回 reward → 冒烟/日志生成可用（订阅额度、无按 token 计费）。可复现性警告：模型版本滚动不透明，不进 E1 主表 | 否（基建） |
| copilot_probe_20260714_101426 | 2026-07-14 | E0.5 | Copilot 后端 chat 阶段：litellm `github_copilot/` 认证+补全通路 | reply='OK', in=12/out=2 tok, 设备流登录一次性（token 缓存本地） | **PASS**：`shared/llm.py` copilot 后端端到端可用，无需 API key | 否（基建） |
| gate1_ceiling_20260705_190509 | 2026-07-05 | Gate1 | 天花板测试(修复后重跑B+C) | A=70%(n=60) C=57.9%(n=38, **22集因账户余额耗尽报错**) | **判定再次无效**(数据污染)。但产出高质量天花板库(library.md 12条, 可零成本复用); 两次 C 均未见提升, 结合文献"朴素堆知识会掉分", "整库注入"路线存疑, 待干净重测或改测"少量精选条目" | 库可复用 |
| gate1_ceiling_20260705_185719 | 2026-07-05 | Gate1 | 天花板测试(续跑B+C) | A=70% C=60% "-10pp" | **判定无效**：fable-5 推理耗尽 max_tokens=1200 输出空库(0字节), chat() 静默返回 → C 实测"空库vs基线"=纯运行噪声。**副产品发现: n=60 时同条件重跑方差可达 ±10pp**, gate 判读需配对+更谨慎 | 否 |
| gate1_ceiling_20260705_185023 | 2026-07-05 | Gate1 | 天花板测试(首跑) | 基线 A=70% (60集, $5.81, 0错误); 30题中12题有失败 | Phase A 完好可复用; Phase B 崩于 fable-5 拒收 temperature 参数(已修 llm.py) | 基线可复用 |
| smoke_tau2_20260705_110319 | 2026-07-05 | E0.1 | 全链路冒烟(修复后) | 5/5 完成; 成功 4/5; $0.094/集(haiku 全角色); 本轮 $0.47 | **PASSED**：tau2+Claude 全链路通; 单集成本实测入 budget_estimate; E0.1 系列累计 ~$0.96 | 否（基建） |
| smoke_tau2_20260705_105714 | 2026-07-05 | E0.1 | 诊断#2 | 2/5 完成; NL 判卷 JSON 解析失败 | 定位: haiku 判卷回复带 markdown 栏, json.loads 裸解析失败 → 加宽容 JSON shim | 否 |
| smoke_tau2_20260705_044317 | 2026-07-05 | E0.1 | 诊断#1 | 2/5 完成; 3 个 infrastructure_error | 定位: tau2 硬编码 gpt-4.1 做 NL_ASSERTIONS 判卷(无 CLI 开关) → 运行时 patch 模块常量 | 否 |
| tau2_probe_20260705_043549 | 2026-07-05 | E0.0 | 零 LLM 验证协议四依赖 | retail=114/airline=50/telecom=114; persona 覆盖 0/114; reward_basis=DB×114+NL×112 | PASSED：事后 evaluate_simulation ✅、PersonaConfig 注入 ✅、env 无 LLM 可建 ✅ →隐藏 verifier 协议与 WildLoop 接地均可实现；persona 需全部自注入（可控性↑） | 否（基建） |
