# CHANGELOG（倒序，每次改动一行；格式见 CONSTITUTION §5）

- 2026-07-05 | REPLAY | E0.0 零 LLM 结构探测通过（tau2_probe_20260705_043549）：事后 verifier ✅、PersonaConfig 注入 ✅、env 无 LLM 可建 ✅；WildLoop persona 风险解除
- 2026-07-05 | shared | 新增 runharness.py（run 目录契约自动化）；llm.py 加 mock 后端；fetch_bib 生成 39 条 refs.bib
- 2026-07-05 | 项目 | τ²-bench clone 并 pin 1901a30，装入 uv 环境（Python 升 3.12，workspace member）；.env 落 key（gitignored）；SSH 公钥已生成待 owner 加 GitHub；origin=git@github.com:huthvincent/skill_opt.git
- 2026-07-05 | 项目 | 初始搭建：目录树、CONSTITUTION、两篇论文骨架（REPLAY / WildLoop）、shared 代码、latex 骨架、uv 环境、git 仓库、文献调研与决策记录入库
