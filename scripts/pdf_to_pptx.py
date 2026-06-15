#!/usr/bin/env python3
"""
pdf_to_pptx.py — 将 Beamer 编译生成的 PDF 转换为 PPTX（高清图片逐页模式）
用法: python pdf_to_pptx.py --input slides.pdf [--output slides.pptx] [--dpi 300]
依赖: PyMuPDF (fitz), python-pptx
"""

import argparse
import sys
import tempfile
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not found. Run: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)

try:
    from pptx import Presentation
    from pptx.util import Inches
except ImportError:
    print("Error: python-pptx not found. Run: pip install python-pptx", file=sys.stderr)
    sys.exit(1)


# 16:9 standard slide size (EMU)
SLIDE_WIDTH_EMU = 12192000   # 33.867cm = 13.333 inches
SLIDE_HEIGHT_EMU = 6858000   # 19.05cm = 7.5 inches
SLIDE_WIDTH_IN = 13.333
SLIDE_HEIGHT_IN = 7.5


def render_page(page, dpi=300):
    """Render a PDF page to a PIL Image at the given DPI using PyMuPDF."""
    mat = fitz.Matrix(dpi / 72, dpi / 72)  # 72 is PDF native DPI
    pix = page.get_pixmap(matrix=mat, alpha=False)
    from PIL import Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    pix = None  # free memory
    return img


def fit_image_to_slide(img, slide_w_px, slide_h_px):
    """Fit image to slide dimensions with center crop (fill + crop)."""
    from PIL import Image
    img_w, img_h = img.size
    img_aspect = img_w / img_h
    slide_aspect = slide_w_px / slide_h_px

    if img_aspect > slide_aspect:
        new_h = slide_h_px
        new_w = int(img_w * (slide_h_px / img_h))
    else:
        new_w = slide_w_px
        new_h = int(img_h * (slide_w_px / img_w))

    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    left = (new_w - slide_w_px) // 2
    top = (new_h - slide_h_px) // 2
    img_cropped = img_resized.crop((left, top, left + slide_w_px, top + slide_h_px))
    img_resized.close()
    return img_cropped


def pdf_to_pptx(input_path, output_path=None, dpi=300):
    """Convert PDF to PPTX using PyMuPDF for high-quality rendering."""
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: PDF not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        output_path = input_path.with_suffix(".pptx")
    else:
        output_path = Path(output_path)

    print(f"Opening PDF: {input_path}")
    doc = fitz.open(str(input_path))
    page_count = doc.page_count
    print(f"  Pages: {page_count}, DPI: {dpi}")

    if page_count == 0:
        print("Error: PDF has no pages", file=sys.stderr)
        sys.exit(1)

    # Create 16:9 PPTX
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH_EMU
    prs.slide_height = SLIDE_HEIGHT_EMU
    blank_layout = prs.slide_layouts[6]  # blank layout

    # Calculate target pixel dimensions from DPI
    slide_w_px = int(dpi * SLIDE_WIDTH_IN)
    slide_h_px = int(dpi * SLIDE_HEIGHT_IN)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(page_count):
            page = doc[i]
            print(f"  Rendering page {i + 1}/{page_count} ...", end="\r")

            img = render_page(page, dpi=dpi)
            img_fitted = fit_image_to_slide(img, slide_w_px, slide_h_px)
            img.close()

            # Save as high-quality PNG
            tmp_png = Path(tmpdir) / f"slide_{i + 1:04d}.png"
            img_fitted.save(str(tmp_png), "PNG", optimize=True)
            img_fitted.close()

            # Insert into PPTX
            slide = prs.slides.add_slide(blank_layout)
            slide.shapes.add_picture(
                str(tmp_png),
                Inches(0), Inches(0),
                Inches(SLIDE_WIDTH_IN), Inches(SLIDE_HEIGHT_IN)
            )

    doc.close()
    prs.save(str(output_path))

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\nDone: {output_path}")
    print(f"  {page_count} slides, {slide_w_px}x{slide_h_px}px, {size_mb:.1f} MB")

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="Convert Beamer PDF to PPTX (high-res image per slide)")
    parser.add_argument("--input", "-i", required=True, help="Input PDF path")
    parser.add_argument("--output", "-o", default=None, help="Output PPTX path (default: same name as PDF)")
    parser.add_argument("--dpi", "-d", type=int, default=300, help="Render DPI (default: 300, use 150 for smaller files)")
    args = parser.parse_args()

    pdf_to_pptx(args.input, args.output, args.dpi)


if __name__ == "__main__":
    main()
