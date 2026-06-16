# SJTUBeamer PPT

基于 [SJTUBeamer](https://github.com/sjtug/SJTUBeamer) 模板的 Claude Code skill，用于生成上海交通大学风格的 LaTeX Beamer 学术幻灯片。

## 功能

- 基于 SJTUBeamer 模板生成高质量学术幻灯片（PDF）
- 支持多种主题预设（答辩、学术报告、组会等）
- 可选将 PDF 转换为 PPTX（图片逐页模式）

## 安装

本 skill 为 Claude Code 全局 skill，位于 `~/.claude/skills/sjtu-beamer-ppt/`。

### 前置依赖

1. **MiKTeX**: `winget install MiKTeX.MiKTeX`
2. 运行环境配置脚本：
   ```powershell
   pwsh -File scripts/setup_env.ps1
   ```
3. **Python 依赖**（仅 PPTX 转换需要）：
   ```bash
   pip install pypdfium2 python-pptx Pillow
   ```

## 使用

在 Claude Code 中说"帮我制作 Beamer 幻灯片"或"用 LaTeX 做一个学术报告 PPT"即可触发。

## 模板

- `basic-lecture.tex` — 通用讲座
- `academic-report.tex` — 学术报告
- `thesis-defense.tex` — 毕业答辩
- `group-meeting.tex` — 组会汇报

## 许可

SJTUBeamer 模板使用 Apache-2.0 许可。校徽资源由上海交通大学持有版权。
