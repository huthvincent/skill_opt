# third_party/ —— 上游仓库

> 只 clone、只读。**绝不修改上游代码**——需要 patch 时，把补丁/包装层放到用它的那篇论文的 `script/` 里。每个仓库固定到具体 commit 并在下表登记，保证换机器可复原。

| 仓库 | 用途 | pin 的 commit | 状态 |
|---|---|---|---|
| `tau2-bench/` (github.com/sierra-research/tau2-bench) | REPLAY 主实验环境（retail/airline/telecom 等 6 域 + user simulator + DB-state verifier） | `1901a301961cbbe3fd11f3e84a2a376530c759e3`（2026-07-01） | ✅ 已 clone，以 uv workspace member 方式装入环境（要求 Python ≥3.12，项目环境已升到 3.12） |

## 复原命令（新机器必须按此顺序：先 clone 再 uv sync，否则 workspace 解析失败）

```bash
cd third_party
git clone https://github.com/sierra-research/tau2-bench
cd tau2-bench && git checkout 1901a301961cbbe3fd11f3e84a2a376530c759e3
cd ../.. && ~/.local/bin/uv sync
```
