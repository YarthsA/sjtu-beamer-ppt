---
name: sjtu-beamer-ppt
description: Create SJTU-style Beamer (LaTeX) presentations using SJTUBeamer template. Use when the user asks for Beamer slides, LaTeX presentations, SJTUBeamer, latex beamer, latex slides, latex presentation, 学术报告 beamer, LaTeX 幻灯片, Beamer 幻灯片, latex-ppt, or wants high-quality typeset SJTU-style presentations with PDF output. Also supports converting compiled PDF to PPTX (image-per-slide) with optional speaker notes. For editable PPTX with SJTU branding, use the sjtu-ppt-template skill instead.
---

# SJTU Beamer PPT

基于 SJTUBeamer 模板，用 LaTeX 生成上海交通大学风格学术幻灯片，支持 PDF + PPTX（含讲稿备注）。

## 典型流程

1. **理解内容 → 选主题**：参考 [references/template-gallery.md](references/template-gallery.md) 选预设
2. **生成 .tex**：遵循 [references/tex-generation-guide.md](references/tex-generation-guide.md)，使用结论式标题
3. **编译 PDF**：`xelatex -interaction=nonstopmode -jobname=tmp main.tex && mv -f tmp.pdf slides.pdf`（用 `-jobname` 避免 PDF 被锁定）
4. **转换 PPTX**：`python scripts/pdf_to_pptx.py --input slides.pdf --output slides.pptx`

### 可选：添加讲稿备注

参考 [references/speaker-notes-guide.md](references/speaker-notes-guide.md)，用 python-pptx 写入备注。

### 可选：图片转换 PPTX

`python scripts/pdf_to_pptx.py --input slides.pdf`

## 预设主题速查

详见 [references/beamer-theme-options.md](references/beamer-theme-options.md) 和 [references/template-gallery.md](references/template-gallery.md)。

| 场景 | 主题 |
|------|------|
| 课程作业/学术报告 | `maxplus,red,light,miniframes` |
| 毕业答辩 | `max,red,dark,infolines` |
| 组会汇报 | `min,blue,light,default` |

## 已知陷阱

1. **`\makebottom`**：SJTUBeamer 自动生成中文"谢谢"结束页，英文 PPT 必须删除
2. **`\institute`**：会占用标题页空间导致溢出，建议删掉
3. **导航栏图标**：`\setbeamertemplate{navigation symbols}{\insertframenumber/\inserttotalframenumber}` 只保留页码
4. **PDF 被锁定**：Windows 阅读器锁文件，用 `-jobname=tmp` 编译后 `mv -f` 覆盖
5. **图片缓存**：`\graphicspath` 可能读到旧版缓存目录，更新图后检查所有搜索路径

## 资源部署

编译时，脚本自动将 `.sty` 文件和 `vi/` 校徽资源从 `assets/SJTUBeamer/` 复制到工作目录。

## 环境要求

- MiKTeX（含 XeLaTeX）: `winget install MiKTeX.MiKTeX`
- Python 依赖（PPTX 转换）: `pip install PyMuPDF python-pptx Pillow`

## 编译参考

详见 [references/compilation-guide.md](references/compilation-guide.md)。

## 与 sjtu-ppt-template 的关系

| 特性 | sjtu-beamer-ppt | sjtu-ppt-template |
|------|-----------------|-------------------|
| 排版引擎 | LaTeX (XeLaTeX) | python-pptx |
| 公式排版 | 完美 | 有限 |
| PPTX 可编辑性 | 图片不可编辑 | 文字可编辑 |
| 适用场景 | 学术报告、论文答辩 | 活动展示、需后期修改 |
