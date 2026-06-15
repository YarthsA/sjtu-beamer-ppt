#!/usr/bin/env python3
"""
preview_slides.py — 将 Beamer PDF 渲染为单独的高清幻灯片图片，用于 Visual QA
用法: python preview_slides.py --input slides.pdf [--output-dir previews/] [--dpi 200]
依赖: PyMuPDF (fitz)
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not found. Run: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)


def preview_slides(input_path, output_dir=None, dpi=200):
    """Render each PDF page as a PNG image using PyMuPDF."""
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: PDF not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if output_dir is None:
        output_dir = input_path.parent / (input_path.stem + "_previews")
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Opening PDF: {input_path}")
    doc = fitz.open(str(input_path))
    page_count = doc.page_count
    print(f"  Pages: {page_count}, DPI: {dpi}")

    for i in range(page_count):
        page = doc[i]
        print(f"  Rendering page {i + 1}/{page_count} ...", end="\r")

        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        out_path = output_dir / f"slide_{i + 1:04d}.png"
        pix.save(str(out_path))
        pix = None  # free memory

    doc.close()
    print(f"\nPreview images saved to: {output_dir}")
    print(f"  {page_count} images at {dpi} DPI")

    return str(output_dir)


def main():
    parser = argparse.ArgumentParser(description="Render Beamer PDF to slide images (for Visual QA)")
    parser.add_argument("--input", "-i", required=True, help="Input PDF path")
    parser.add_argument("--output-dir", "-o", default=None, help="Output directory (default: <pdf>_previews/)")
    parser.add_argument("--dpi", "-d", type=int, default=200, help="Render DPI (default: 200)")
    args = parser.parse_args()

    preview_slides(args.input, args.output_dir, args.dpi)


if __name__ == "__main__":
    main()
