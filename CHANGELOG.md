# CHANGELOG（倒序，每次改动一行；格式见 CONSTITUTION §5）

- 2026-07-06 | docs | benchmark 选择核实: tau2 确认主选(retail+telecom 划分, airline=50 太小降 OOD); 加 AppWorld 作第二 benchmark(正式实验); refs 增至 47 条

- 2026-07-06 | 项目 | CAGE 主线定案(owner 拍板): PROPOSAL v2 + method.md v3 重写为对抗共进化+认证终点; MVP 指令文档待 owner 答疑后推 GAA.git
- 2026-07-06 | 项目 | 外部评审裁定完成(docs/review_response_20260706.md): LCB Wald bug 修复(shared/stats.py, 0/3→3/3 正解+18.4pp); WISE-Flow/GRASP/judge-AUROC 一手核实(refs.bib 增至43条); 设定重构三选一待 owner; 放弃 AAAI-27 定案; **另一台 server 的 pilot 产物未 push, 待补**

- 2026-07-05 | 项目 | git 历史二次重写：作者邮箱统一为 GitHub noreply 地址(11199893+huthvincent@users.noreply.github.com)保证归属显示; force push(owner 授权); 旧 clone 需重新 clone

- 2026-07-05 | docs | 新增 trans.md 跨机器交接文档（新 server 冷启动全指南）；owner 将在另一台机器 clone 并用新 API 跑 sanity check v2

- 2026-07-05 | docs | 新增 method.md（通俗方法讲解+对比）与 sanity_check.md（$100 内 4 门 go/no-go 验证计划）
- 2026-07-05 | 项目 | git 历史重写：3 个 commit 作者统一为 huthvincent <huthruiz@gmail.com>，修复乱码 commit message，force push（owner 授权的一次性操作）

- 2026-07-05 | REPLAY | E0.1 通过（smoke_tau2_20260705_110319，4/5 成功，$0.094/集，系列累计 ~$0.96/$10 上限）；两处运行时 patch 化解 tau2 的 gpt-4.1 硬编码（NL 判卷模型 + JSON 解析）；Doc/budget_estimate.md v0 初稿（全论文混合方案 ~$2,000）
- 2026-07-05 | 项目 | GitHub 私有远程接通并首推（git@github.com:huthvincent/skill_opt.git, main 分支）

- 2026-07-05 | REPLAY | E0.0 零 LLM 结构探测通过（tau2_probe_20260705_043549）：事后 verifier ✅、PersonaConfig 注入 ✅、env 无 LLM 可建 ✅；WildLoop persona 风险解除
- 2026-07-05 | shared | 新增 runharness.py（run 目录契约自动化）；llm.py 加 mock 后端；fetch_bib 生成 39 条 refs.bib
- 2026-07-05 | 项目 | τ²-bench clone 并 pin 1901a30，装入 uv 环境（Python 升 3.12，workspace member）；.env 落 key（gitignored）；SSH 公钥已生成待 owner 加 GitHub；origin=git@github.com:huthvincent/skill_opt.git
- 2026-07-05 | 项目 | 初始搭建：目录树、CONSTITUTION、两篇论文骨架（REPLAY / WildLoop）、shared 代码、latex 骨架、uv 环境、git 仓库、文献调研与决策记录入库
