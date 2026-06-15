# PDF → PPTX 转换指南

## 概述

编译 Beamer 幻灯片后，可将 PDF 转换为 PPTX 格式以便在 PowerPoint/WPS 中打开或投影。

**核心方法**: 将 PDF 每页渲染为高清图片，然后逐页插入 PPTX 幻灯片。

## 重要限制

⚠️ **转换后的 PPTX 中，每页是一张完整图片，文字不可编辑。**

- PDF 是权威输出，PPTX 是辅助输出
- 如果用户需要 **可编辑的 PPTX**（文字、形状可修改），应该使用 `sjtu-ppt-template` skill（python-pptx 方案）
- 本方案适用于：最终定稿后需要 PPTX 格式投影、或在没有 LaTeX 环境的电脑上演示

## 转换命令

### 基本转换

```bash
python scripts/pdf_to_pptx.py --input slides.pdf
```

### 指定输出和分辨率

```bash
python scripts/pdf_to_pptx.py --input slides.pdf --output presentation.pptx --scale 2
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` / `-i` | (必填) | 输入 PDF 路径 |
| `--output` / `-o` | 与 PDF 同名 | 输出 PPTX 路径 |
| `--scale` / `-s` | 2 | 渲染倍率（2 = 1920px 宽，3 = 2880px 宽） |

## 渲染质量

| 倍率 | 分辨率 | 文件大小 | 适用场景 |
|------|--------|----------|----------|
| 1x | ~960px 宽 | 小 | 快速预览 |
| 2x | ~1920px 宽 | 中 | 日常投影（推荐） |
| 3x | ~2880px 宽 | 大 | 打印、高清显示 |

## 图片适配策略

Beamer PDF 页面比例固定为 16:9（当使用 `aspectratio=169` 时），与 PPTX 幻灯片一致。脚本会：

1. 渲染 PDF 页面为 PNG
2. 居中裁剪到精确的 16:9 比例
3. 插入 PPTX 全屏尺寸

## 依赖库

```bash
pip install pypdfium2 python-pptx Pillow
```

- `pypdfium2`: PDF 渲染（自带渲染引擎，无需外部 poppler）
- `python-pptx`: PPTX 生成
- `Pillow`: 图片处理

## Visual QA（预览检查）

转换前可用 `preview_slides.py` 生成预览图片进行视觉检查：

```bash
python scripts/preview_slides.py --input slides.pdf --output-dir previews/
```

这会生成 `previews/slide_0001.png` 等图片文件，可以逐页检查排版质量。

## 与 sjtu-ppt-template 的区别

| 特性 | sjtu-beamer-ppt (本方案) | sjtu-ppt-template |
|------|--------------------------|-------------------|
| 排版引擎 | LaTeX (XeLaTeX) | python-pptx |
| 公式排版 | 完美支持 | 有限 |
| 输出格式 | PDF (主) + PPTX (辅) | PPTX |
| PPTX 可编辑性 | ❌ 图片不可编辑 | ✅ 文字/形状可编辑 |
| 适用场景 | 学术报告、论文答辩 | 活动展示、需要后期修改 |
| 制作速度 | 首次编译较慢 | 较快 |
