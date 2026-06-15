---
name: sjtu-beamer-ppt
description: Create SJTU-style Beamer (LaTeX) presentations using SJTUBeamer template. Use when the user asks for Beamer slides, LaTeX presentations, SJTUBeamer, latex beamer, latex slides, latex presentation, 学术报告 beamer, LaTeX 幻灯片, Beamer 幻灯片, latex-ppt, or wants high-quality typeset SJTU-style presentations with PDF output. Also supports converting compiled PDF to PPTX (image-per-slide). For editable PPTX with SJTU branding, use the sjtu-ppt-template skill instead.
---

# SJTU Beamer PPT

基于 SJTUBeamer 模板，用 LaTeX 生成高质量的上海交通大学风格学术幻灯片，支持输出 PDF 和 PPTX。

本 skill 适合需要 **高质量排版**（数学公式、代码高亮、精确字体）的学术场景。如果用户需要 **可编辑的 PPTX**，请使用 `sjtu-ppt-template` skill。

## Quick Start

### 1. 检查环境

```powershell
pwsh -File scripts/check_env.ps1
```

如果环境未就绪，运行安装脚本：

```powershell
pwsh -File scripts/setup_env.ps1
```

或手动安装：`! winget install MiKTeX.MiKTeX`，然后运行 `scripts/setup_env.ps1` 完成配置。

### 2. 理解用户内容，选择主题

根据使用场景选择预设，参考 [references/template-gallery.md](references/template-gallery.md)。

### 3. 生成 .tex 文件

基于 [references/tex-generation-guide.md](references/tex-generation-guide.md) 中的规范，选择合适的模板并填充内容。

### 4. 编译

```powershell
pwsh -File scripts/compile_tex.ps1 -TexFile main.tex -WorkDir /path/to/project
```

### 5. 可选：转换为 PPTX

```bash
python scripts/pdf_to_pptx.py --input slides.pdf --output slides.pptx
```

## 主题选项

修改 `\usetheme[选项]{sjtubeamer}` 中的选项切换风格。

详细参考 [references/beamer-theme-options.md](references/beamer-theme-options.md)。

**速查：**
- 封面：`maxplus`(现代) / `max`(经典) / `min`(极简)
- 颜色：`red`(交大红) / `blue`(交大蓝)
- 亮度：`light`(浅色) / `dark`(深色)
- 导航栏：`miniframes` / `infolines` / `sidebar` / `default` / `smoothbars` 等
- 校徽位置：`topright` / `bottomright`

## 工作流程

1. **分析用户需求**：确定场景（答辩、报告、组会等），选择对应模板
2. **选择预设主题**：参考 [references/template-gallery.md](references/template-gallery.md)
3. **生成 .tex**：
   - 从 `templates/` 目录选择合适的模板
   - 遵循 [references/tex-generation-guide.md](references/tex-generation-guide.md) 的规范
   - 将用户内容转化为 Beamer frame 结构
   - 使用结论式标题（非话题式）
4. **编译为 PDF**：使用 `scripts/compile_tex.ps1`
5. **视觉检查**：用 `scripts/preview_slides.py` 生成预览图，检查排版
6. **可选转换**：用 `scripts/pdf_to_pptx.py` 生成 PPTX
7. **交付用户**：告知 PDF 和 PPTX 文件路径

## 模板选择

| 场景 | 模板文件 | 主题预设 |
|------|----------|----------|
| 通用讲座 | `templates/basic-lecture.tex` | `maxplus,red,light` |
| 学术报告 | `templates/academic-report.tex` | `maxplus,red,light` |
| 毕业答辩 | `templates/thesis-defense.tex` | `max,red,dark` |
| 组会汇报 | `templates/group-meeting.tex` | `min,blue,light` |

## 资源部署

编译时，脚本会自动将 `.sty` 文件和 `vi/` 校徽资源从 `assets/SJTUBeamer/` 复制到工作目录。

## 与 sjtu-ppt-template 的关系

| 特性 | sjtu-beamer-ppt（本 skill） | sjtu-ppt-template |
|------|-----------------------------|-------------------|
| 排版引擎 | LaTeX (XeLaTeX) | python-pptx |
| 公式排版 | ⭐ 完美 | 有限 |
| PPTX 可编辑性 | ❌ 图片不可编辑 | ✅ 文字可编辑 |
| 适用场景 | 学术报告、论文答辩、公式密集 | 活动展示、需后期修改 |

**建议**：如果用户未明确要求 Beamer/LaTeX，优先推荐 `sjtu-ppt-template`（更通用）。当内容涉及大量数学公式、代码、或用户明确要求 Beamer 时，使用本 skill。

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `scripts/check_env.ps1` | 检测编译环境（MiKTeX、XeLaTeX、latexmk） |
| `scripts/setup_env.ps1` | 首次配置：安装 MiKTeX、配置自动安装、克隆模板 |
| `scripts/compile_tex.ps1` | 编译 .tex 为 PDF（部署资源 + latexmk） |
| `scripts/pdf_to_pptx.py` | PDF → PPTX 图片逐页转换 |
| `scripts/preview_slides.py` | PDF → 图片序列（用于 Visual QA） |

## 依赖

### 编译环境
- MiKTeX（含 XeLaTeX）
- latexmk（`mpm --install latexmk`）

### Python 依赖（PPTX 转换）
```bash
pip install pypdfium2 python-pptx Pillow
```

## Quality Gates

编译后检查：

- PDF 是否成功生成且非空
- 封面页标题、作者、日期是否正确
- 中文是否正常显示（无乱码/方框）
- 公式是否正确渲染
- 代码块是否正确高亮
- 图片是否正确插入且未溢出
- 节目录页是否正确生成
- 页数是否符合预期
