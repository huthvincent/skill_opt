# data/ —— 共享数据目录

> 本目录**不进 git**（.gitignore 已配）。换机器后按下面的"如何复原"重建。规则见 CONSTITUTION §4.3、§9。

## 子目录

| 目录 | 内容 | 读写规则 |
|---|---|---|
| `raw/` | 下载的公开数据集原件（WildChat、LMSYS-Chat-1M 等） | **只读**，永不修改 |
| `generated_logs/` | 弱 agent × persona-simulator 批量生成的"历史交互日志"（REPLAY 的离线语料） | 只由生成脚本写入，每批一个子目录，命名同 run_id 规范 |

## 如何复原（新机器 checklist）

| 数据 | 复原方式 | 状态 |
|---|---|---|
| WildChat-1M | `huggingface-cli download allenai/WildChat-1M --repo-type dataset` → `raw/wildchat/`（需同意 HF 上的使用条款） | ⬜ 尚未下载 |
| LMSYS-Chat-1M | 同上，`lmsys/lmsys-chat-1m`（需申请访问） | ⬜ 尚未下载 |
| 生成日志 | 跑 `REPLAY/script/gen_logs_*.py`（脚本尚未写；生成参数会记录在对应 `results/<run_id>/config.json`） | ⬜ 管线未建 |

**登记规则**：任何新数据进入本目录，必须同时在上表加一行（是什么、怎么复原、多大）。
