#!/usr/bin/env python3
"""
pdf_to_pptx.py — 将 Beamer 编译生成的 PDF 转换为 PPTX（图片逐页模式）
用法: python pdf_to_pptx.py --input slides.pdf [--output slides.pptx] [--scale 2]
依赖: pypdfium2, python-pptx, Pillow
"""

import argparse
import sys
import tempfile
from pathlib import Path

try:
    import pypdfium2 as pdfium
except ImportError:
    print("错误: 需要 pypdfium2。运行: pip install pypdfium2", file=sys.stderr)
    sys.exit(1)

try:
    from pptx import Presentation
    from pptx.util import Inches
except ImportError:
    print("错误: 需要 python-pptx。运行: pip install python-pptx", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("错误: 需要 Pillow。运行: pip install Pillow", file=sys.stderr)
    sys.exit(1)


# 16:9 标准幻灯片尺寸 (EMU)
SLIDE_WIDTH_EMU = 12192000   # 33.867cm = 13.333 inches
SLIDE_HEIGHT_EMU = 6858000   # 19.05cm = 7.5 inches
SLIDE_WIDTH_IN = 13.333
SLIDE_HEIGHT_IN = 7.5
SLIDE_ASPECT = SLIDE_WIDTH_IN / SLIDE_HEIGHT_IN  # ~1.778


def render_page_to_image(page, scale=2):
    """将 PDF 页面渲染为 PIL Image"""
    bitmap = page.render(scale=scale)
    pil_image = bitmap.to_pil()
    bitmap.close()
    return pil_image


def fit_image_to_slide(img, slide_w_px, slide_h_px):
    """
    将图片适配到幻灯片尺寸。
    策略：保持比例，居中裁剪（fill + center crop）。
    """
    img_w, img_h = img.size
    img_aspect = img_w / img_h
    slide_aspect = slide_w_px / slide_h_px

    if img_aspect > slide_aspect:
        # 图片更宽：按高度适配，裁剪左右
        new_h = slide_h_px
        new_w = int(img_w * (slide_h_px / img_h))
    else:
        # 图片更高：按宽度适配，裁剪上下
        new_w = slide_w_px
        new_h = int(img_h * (slide_w_px / img_w))

    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    # 居中裁剪
    left = (new_w - slide_w_px) // 2
    top = (new_h - slide_h_px) // 2
    img_cropped = img_resized.crop((left, top, left + slide_w_px, top + slide_h_px))

    return img_cropped


def pdf_to_pptx(input_path, output_path=None, scale=2):
    """将 PDF 转换为 PPTX"""
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"错误: PDF 文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        output_path = input_path.with_suffix(".pptx")
    else:
        output_path = Path(output_path)

    print(f"正在打开 PDF: {input_path}")
    doc = pdfium.PdfDocument(str(input_path))
    page_count = len(doc)
    print(f"  共 {page_count} 页")

    if page_count == 0:
        print("错误: PDF 没有页面", file=sys.stderr)
        sys.exit(1)

    # 创建 16:9 PPTX
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH_EMU
    prs.slide_height = SLIDE_HEIGHT_EMU
    blank_layout = prs.slide_layouts[6]  # blank layout

    # 渲染分辨率：宽度目标像素 = scale * 96 * 13.333 ≈ 1920@2x
    slide_w_px = int(96 * SLIDE_WIDTH_IN * scale)
    slide_h_px = int(96 * SLIDE_HEIGHT_IN * scale)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(page_count):
            page = doc[i]
            print(f"  渲染第 {i + 1}/{page_count} 页 ...", end="\r")

            img = render_page_to_image(page, scale=scale)
            img_fitted = fit_image_to_slide(img, slide_w_px, slide_h_px)

            # 保存临时 PNG
            tmp_png = Path(tmpdir) / f"slide_{i + 1:04d}.png"
            img_fitted.save(str(tmp_png), "PNG", optimize=True)

            img.close()
            img_fitted.close()

            # 插入 PPTX
            slide = prs.slides.add_slide(blank_layout)
            slide.shapes.add_picture(
                str(tmp_png),
                Inches(0), Inches(0),
                Inches(SLIDE_WIDTH_IN), Inches(SLIDE_HEIGHT_IN)
            )

    doc.close()

    prs.save(str(output_path))
    print(f"\n转换完成: {output_path}")
    print(f"  共 {page_count} 页幻灯片，分辨率 {slide_w_px}x{slide_h_px}px")

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="将 Beamer PDF 转换为 PPTX（图片逐页）")
    parser.add_argument("--input", "-i", required=True, help="输入 PDF 文件路径")
    parser.add_argument("--output", "-o", default=None, help="输出 PPTX 文件路径（默认与 PDF 同名）")
    parser.add_argument("--scale", "-s", type=float, default=2, help="渲染倍率（默认 2，即 2x 分辨率）")
    args = parser.parse_args()

    pdf_to_pptx(args.input, args.output, args.scale)


if __name__ == "__main__":
    main()
