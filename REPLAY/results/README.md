# REPLAY/results/ —— 实验输出（只由脚本写入）

- 每次运行一个子目录：`results/<run_id>/`，run_id = `<script>_<YYYYMMDD_HHMMSS>`。
- 必含：`config.json`（全部参数 + git commit hash）、`log.txt`、`REPORT.md`（自动生成：配置摘要 + 指标表 + 一句话结论）。
- 中间产物放 `<run_id>/cache/`（不进 git，可删）；**run 目录本身永不删除**（CONSTITUTION §9）。
- 想知道某次实验的结论 → 直接看该 run 的 `REPORT.md`；想看全局 → `../LEDGER.md`。
