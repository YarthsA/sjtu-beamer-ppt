# SJTU Beamer PPT — Claude Code Skill

基于 [SJTUBeamer](https://github.com/sjtug/SJTUBeamer) 的 Claude Code skill，用于生成上海交通大学风格的 LaTeX Beamer 学术幻灯片，支持 PDF 和 PPTX 双格式输出。

## 功能

- 🎓 **LaTeX 排版** — 数学公式、代码高亮、精确字体，学术幻灯片的最佳排版质量
- 🎨 **SJTUBeamer 主题** — 内置完整模板，支持多种封面/配色/导航栏样式
- 📄 **PDF 输出** — 编译生成高质量 16:9 PDF 幻灯片
- 📊 **PPTX 转换** — 自动检测最佳引擎，优先生成可编辑 PPTX
- 📝 **4 个模板** — 讲座、学术报告、毕业答辩、组会汇报

## PDF → PPTX 转换策略

脚本按优先级自动检测可用引擎：

```
1. WPS pdf2ppt (AI)    → 文字可编辑，需安装 WPS Office
2. WPS pdf2ppt (basic) → 文字可编辑，更快
3. PyMuPDF 图片模式    → 通用兜底，任何平台可用
```

| 引擎 | 文字可编辑 | 依赖 | 速度 |
|------|-----------|------|------|
| WPS AI | ✅ | WPS Office（免费版即可） | ~12s |
| WPS basic | ✅ | WPS Office（免费版即可） | ~3s |
| PyMuPDF | ❌ 图片 | pip install PyMuPDF | ~10s |

**没有 WPS？** PyMuPDF 引擎会自动接管，生成 300 DPI 高清图片 PPTX。

## 安装

### 方式一：作为 Claude Code skill 安装（推荐）

```bash
git clone https://github.com/YarthsA/sjtu-beamer-ppt.git ~/.claude/skills/sjtu-beamer-ppt
```

然后安装 LaTeX 环境：

```bash
# 安装 MiKTeX
winget install MiKTeX.MiKTeX

# 运行环境配置（配置自动安装包、安装 latexmk）
pwsh -File ~/.claude/skills/sjtu-beamer-ppt/scripts/setup_env.ps1
```

安装 Python 依赖（PPTX 转换需要）：

```bash
pip install PyMuPDF python-pptx Pillow
```

### 方式二：手动使用

```bash
git clone https://github.com/YarthsA/sjtu-beamer-ppt.git
cd sjtu-beamer-ppt
```

确保已安装 MiKTeX + XeLaTeX + latexmk，然后：

```bash
# 编译
pwsh -File scripts/compile_tex.ps1 -TexFile templates/basic-lecture.tex -WorkDir .

# 转换 PPTX
python scripts/pdf_to_pptx.py --input templates/basic-lecture.pdf
```

## 使用

### 在 Claude Code 中

在 Claude Code 中说以下任意一句即可触发：

- "帮我用 Beamer 做一个学术报告 PPT"
- "制作 Beamer 幻灯片"
- "用 LaTeX 做答辩 PPT"

### 命令行

```bash
# 编译 .tex 为 PDF
pwsh -File scripts/compile_tex.ps1 -TexFile main.tex -WorkDir /path/to/project

# PDF → PPTX（自动选择引擎）
python scripts/pdf_to_pptx.py --input slides.pdf

# PDF → PPTX（指定引擎）
python scripts/pdf_to_pptx.py --input slides.pdf --engine wps       # 强制 WPS
python scripts/pdf_to_pptx.py --input slides.pdf --engine pymupdf   # 强制 PyMuPDF

# 生成预览图（Visual QA）
python scripts/preview_slides.py --input slides.pdf --dpi 200
```

## 模板

| 模板 | 场景 | 主题 |
|------|------|------|
| `templates/basic-lecture.tex` | 通用讲座 | 默认 (maxplus, red, light) |
| `templates/academic-report.tex` | 学术报告 | 默认 |
| `templates/thesis-defense.tex` | 毕业答辩 | 默认 |
| `templates/group-meeting.tex` | 组会汇报 | 默认 |

### 切换主题

修改 `\usetheme` 参数：

```latex
\usetheme{sjtubeamer}                          % 默认: maxplus, red, light
\usetheme[max,blue,dark]{sjtubeamer}           % 经典蓝色深色
\usetheme[min,blue,light,shadow]{sjtubeamer}   % 极简蓝色阴影导航
```

可选值：

| 选项组 | 值 |
|--------|-----|
| 封面 | `maxplus`(现代) / `max`(经典) / `min`(极简) |
| 颜色 | `red`(交大红) / `blue`(交大蓝) |
| 亮度 | `light` / `dark` |
| 导航栏 | `miniframes` / `infolines` / `sidebar` / `shadow` / `smoothbars` 等 |
| 校徽位置 | `topright` / `bottomright` |

## 目录结构

```
sjtu-beamer-ppt/
├── SKILL.md                    # Claude Code skill 入口
├── README.md
├── ASSET_NOTICE.md             # 许可声明
├── assets/
│   └── SJTUBeamer/             # SJTUBeamer v3.2.0 模板
├── scripts/
│   ├── check_env.ps1           # 环境检测
│   ├── setup_env.ps1           # 首次配置
│   ├── compile_tex.ps1         # .tex → PDF 编译
│   ├── pdf_to_pptx.py          # PDF → PPTX 转换
│   └── preview_slides.py       # PDF → 预览图
├── templates/                  # .tex 模板文件
└── references/                 # 参考文档
    ├── beamer-theme-options.md # 主题选项速查
    ├── template-gallery.md     # 预设主题组合
    ├── tex-generation-guide.md # .tex 编写指南
    ├── compilation-guide.md    # 编译排错
    └── pdf-to-pptx-conversion.md # 转换说明
```

## 依赖

### 必需

- **MiKTeX**（含 XeLaTeX）— `winget install MiKTeX.MiKTeX`
- **latexmk** — `mpm --install latexmk`

### Python（PPTX 转换）

```bash
pip install PyMuPDF python-pptx Pillow
```

### 可选

- **WPS Office** — 提供可编辑 PPTX 输出（免费版即可，从 [wps.cn](https://www.wps.cn/) 下载）

## 与 sjtu-ppt-template 的关系

本项目与 [sjtu-ppt-template](~/.claude/skills/sjtu-ppt-template)（python-pptx 方案）并存：

| 特性 | sjtu-beamer-ppt | sjtu-ppt-template |
|------|----------------|-------------------|
| 排版引擎 | LaTeX (XeLaTeX) | python-pptx |
| 公式排版 | ⭐ 完美 | 有限 |
| PPTX 可编辑 | ⚠️ 需 WPS | ✅ 完全可编辑 |
| 适用场景 | 学术报告、公式密集 | 活动展示、需后期修改 |

## 许可

- SJTUBeamer 模板：[Apache-2.0](https://github.com/sjtug/SJTUBeamer/blob/main/LICENSE)
- SJTU 视觉形象（校徽等）：© 上海交通大学，使用须遵循 [视觉形象管理规定](https://vi.sjtu.edu.cn)
- 本 skill 代码：MIT
