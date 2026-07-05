# REPLAY/latex/ —— 论文源文件

- 编译：`latexmk -pdf main.tex`（本目录下执行；产物 main.pdf 不进 git）。
- 结构：`main.tex` 只放 preamble 和 `\input`；正文全在 `sections/`；图放 `figures/`。
- `refs.bib` 由 `shared/fetch_bib.py` **自动生成，不许手改**；arXiv 上没有的文献（书、网页）手工加到本目录 `extra_refs.bib`（生成器会自动拼接）。
- 模板：通用 arXiv preprint（决策 #6）；venue 定稿（ICLR-27 模板发布）后再换。
- 写作红线：实验数字只能来自 `results/<run_id>/REPORT.md`（经 LEDGER 可溯源）；未验证论断必须裹 `\todo{}`。
- 给合作者：`latexmk -C && zip -r replay_overleaf.zip . -x "*.git*"` 后上传 Overleaf；拉回的改动 diff 后合入本目录（仓库是唯一真源）。
