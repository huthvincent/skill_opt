# third_party/ —— 上游仓库

> 只 clone、只读。**绝不修改上游代码**——需要 patch 时，把补丁/包装层放到用它的那篇论文的 `script/` 里。每个仓库固定到具体 commit 并在下表登记，保证换机器可复原。

| 仓库 | 用途 | pin 的 commit | 状态 |
|---|---|---|---|
| `tau2-bench/` (github.com/sierra-research/tau2-bench) | REPLAY 主实验环境（retail/airline/telecom + user simulator + DB-state verifier） | 待 clone 时登记 | ⬜ 待 clone（REPLAY 冒烟第一步） |

## 复原命令模板

```bash
cd third_party
git clone https://github.com/sierra-research/tau2-bench
cd tau2-bench && git checkout <上表登记的 commit>
```
