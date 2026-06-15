# PDF → PPTX 转换指南

## 概述

编译 Beamer 幻灯片后，可将 PDF 转换为 PPTX 格式以便在 PowerPoint/WPS 中打开或投影。

## 转换引擎

脚本按优先级自动检测可用引擎：

| 优先级 | 引擎 | 文字可编辑 | 依赖 | 说明 |
|--------|------|-----------|------|------|
| 1 | WPS pdf2ppt (AI) | ✅ | WPS Office | 质量最好，需本地安装 WPS |
| 2 | WPS pdf2ppt (basic) | ✅ | WPS Office | 更快，需本地安装 WPS |
| 3 | PyMuPDF (图片) | ❌ | pip install PyMuPDF | 通用兜底，任何平台可用 |

**WPS 是可选增强**：没有 WPS 时自动回退到 PyMuPDF 图片模式。

## 转换命令

### 自动模式（推荐）

```bash
python scripts/pdf_to_pptx.py --input slides.pdf
```

### 指定引擎

```bash
python scripts/pdf_to_pptx.py --input slides.pdf --engine wps       # 强制 WPS
python scripts/pdf_to_pptx.py --input slides.pdf --engine pymupdf   # 强制 PyMuPDF
```

### 指定 DPI（仅 PyMuPDF 模式）

```bash
python scripts/pdf_to_pptx.py --input slides.pdf --engine pymupdf --dpi 300
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` / `-i` | (必填) | 输入 PDF 路径 |
| `--output` / `-o` | 与 PDF 同名 | 输出 PPTX 路径 |
| `--engine` / `-e` | `auto` | 转换引擎 |
| `--dpi` / `-d` | 300 | PyMuPDF 渲染 DPI |

## WPS 引擎（可选，产生可编辑 PPTX）

如果系统安装了 WPS Office，脚本会自动检测并优先使用 `kwpsconvert.exe pdf2ppt`。

**效果**：
- 文字是 PowerPoint 原生文本框，可直接编辑
- 公式和图片转为嵌入图片（合理限制）
- 转换速度 4~12 秒

**要求**：
- 本地安装 WPS Office

**安装 WPS**（可选）：
- Windows: 从 https://www.wps.cn/ 下载安装
- 安装后脚本自动检测，无需额外配置

## PyMuPDF 引擎（通用兜底）

任何平台都可用，只需 pip 安装：

```bash
pip install PyMuPDF python-pptx Pillow
```

**效果**：
- 每页 PDF 渲染为高分辨率 PNG 图片
- 插入 PPTX 作为全屏背景图
- 文字不可编辑，但视觉效果清晰

## Visual QA（预览检查）

```bash
python scripts/preview_slides.py --input slides.pdf --output-dir previews/ --dpi 200
```

## 与 sjtu-ppt-template 的区别

| 特性 | sjtu-beamer-ppt (本方案) | sjtu-ppt-template |
|------|--------------------------|-------------------|
| 排版引擎 | LaTeX (XeLaTeX) | python-pptx |
| 公式排版 | 完美支持 | 有限 |
| PPTX 可编辑性 | ⚠️ WPS: 文字可编辑 / PyMuPDF: 图片 | ✅ 完全可编辑 |
| 适用场景 | 学术报告、公式密集 | 活动展示、需要后期修改 |
