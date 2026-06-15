#!/usr/bin/env python3
"""
preview_slides.py — 将 Beamer PDF 渲染为单独的幻灯片图片，用于 Visual QA
用法: python preview_slides.py --input slides.pdf [--output-dir previews/] [--scale 2]
依赖: pypdfium2, Pillow
"""

import argparse
import sys
from pathlib import Path

try:
    import pypdfium2 as pdfium
except ImportError:
    print("错误: 需要 pypdfium2。运行: pip install pypdfium2", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("错误: 需要 Pillow。运行: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def preview_slides(input_path, output_dir=None, scale=2):
    """将 PDF 每页渲染为 PNG 图片"""
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"错误: PDF 文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    if output_dir is None:
        output_dir = input_path.parent / (input_path.stem + "_previews")
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"正在打开 PDF: {input_path}")
    doc = pdfium.PdfDocument(str(input_path))
    page_count = len(doc)
    print(f"  共 {page_count} 页，渲染倍率: {scale}x")

    for i in range(page_count):
        page = doc[i]
        print(f"  渲染第 {i + 1}/{page_count} 页 ...", end="\r")

        bitmap = page.render(scale=scale)
        pil_image = bitmap.to_pil()
        bitmap.close()

        out_path = output_dir / f"slide_{i + 1:04d}.png"
        pil_image.save(str(out_path), "PNG", optimize=True)
        pil_image.close()

    doc.close()
    print(f"\n预览图片已保存到: {output_dir}")
    print(f"  共 {page_count} 张图片")

    return str(output_dir)


def main():
    parser = argparse.ArgumentParser(description="将 Beamer PDF 渲染为幻灯片图片（用于 Visual QA）")
    parser.add_argument("--input", "-i", required=True, help="输入 PDF 文件路径")
    parser.add_argument("--output-dir", "-o", default=None, help="输出图片目录（默认: <pdf名>_previews/）")
    parser.add_argument("--scale", "-s", type=float, default=2, help="渲染倍率（默认 2）")
    args = parser.parse_args()

    preview_slides(args.input, args.output_dir, args.scale)


if __name__ == "__main__":
    main()
