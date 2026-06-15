#!/usr/bin/env python3
"""
pdf_to_pptx.py — 将 Beamer PDF 转换为 PPTX
优先使用 WPS 本地转换（文字可编辑），回退到 PyMuPDF 图片模式。

用法:
  python pdf_to_pptx.py --input slides.pdf                    # 自动选择最佳方式
  python pdf_to_pptx.py --input slides.pdf --engine wps       # 强制 WPS
  python pdf_to_pptx.py --input slides.pdf --engine pymupdf   # 强制 PyMuPDF 图片
  python pdf_to_pptx.py --input slides.pdf --engine wps-basic # WPS basic 模式（更快）
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# WPS kwpsconvert.exe 路径候选
WPS_CANDIDATES = [
    r"D:\WPS Office\12.1.0.26895\office6\kwpsconvert.exe",
    r"D:\WPS Office\12.1.0.26375\office6\kwpsconvert.exe",
    r"C:\Program Files\kingsoft\office6\kwpsconvert.exe",
]


def find_wps():
    """查找本地 WPS kwpsconvert.exe"""
    for p in WPS_CANDIDATES:
        if Path(p).exists():
            return p
    # 尝试 PATH
    return shutil.which("kwpsconvert")


def convert_wps(pdf_path, output_path, engine="ai"):
    """使用 WPS 本地转换 PDF → PPTX（文字可编辑）"""
    wps = find_wps()
    if not wps:
        return False, "WPS kwpsconvert.exe not found"

    cmd = [
        wps, "pdf2ppt",
        str(pdf_path),
        "-o", str(output_path),
        "--engine", engine,
        "--image-quality", "best",
    ]

    print(f"  Using WPS ({engine} mode) ...")
    result = subprocess.run(cmd, capture_output=True, timeout=300)
    stdout = result.stdout.decode("utf-8", errors="replace") if result.stdout else ""
    stderr = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""

    if result.returncode == 0 and output_path.exists():
        return True, None
    elif result.returncode in (100, 101):
        return False, "WPS requires VIP account"
    else:
        msg = stdout.strip() or stderr.strip() or f"exit code {result.returncode}"
        return False, msg


def convert_pymupdf(pdf_path, output_path, dpi=300):
    """使用 PyMuPDF 渲染图片逐页插入 PPTX（不可编辑，但清晰）"""
    try:
        import fitz
        from PIL import Image
        from pptx import Presentation
        from pptx.util import Inches
    except ImportError as e:
        return False, f"Missing dependency: {e}"

    doc = fitz.open(str(pdf_path))
    page_count = doc.page_count
    if page_count == 0:
        doc.close()
        return False, "PDF has no pages"

    # 16:9 standard slide size (EMU)
    SLIDE_W_EMU = 12192000
    SLIDE_H_EMU = 6858000
    SLIDE_W_IN = 13.333
    SLIDE_H_IN = 7.5

    prs = Presentation()
    prs.slide_width = SLIDE_W_EMU
    prs.slide_height = SLIDE_H_EMU
    blank_layout = prs.slide_layouts[6]

    slide_w_px = int(dpi * SLIDE_W_IN)
    slide_h_px = int(dpi * SLIDE_H_IN)

    print(f"  Using PyMuPDF ({dpi} DPI, image mode) ...")

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(page_count):
            page = doc[i]
            print(f"  Rendering page {i + 1}/{page_count} ...", end="\r")

            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pix = None

            # Center crop to 16:9
            iw, ih = img.size
            ia = iw / ih
            sa = slide_w_px / slide_h_px
            if ia > sa:
                nw, nh = int(iw * slide_h_px / ih), slide_h_px
            else:
                nw, nh = slide_w_px, int(ih * slide_w_px / iw)
            img_r = img.resize((nw, nh), Image.LANCZOS)
            img.close()
            l, t = (nw - slide_w_px) // 2, (nh - slide_h_px) // 2
            img_c = img_r.crop((l, t, l + slide_w_px, t + slide_h_px))
            img_r.close()

            tmp_png = Path(tmpdir) / f"s_{i + 1:04d}.png"
            img_c.save(str(tmp_png), "PNG", optimize=True)
            img_c.close()

            slide = prs.slides.add_slide(blank_layout)
            slide.shapes.add_picture(str(tmp_png), Inches(0), Inches(0),
                                     Inches(SLIDE_W_IN), Inches(SLIDE_H_IN))

    doc.close()
    prs.save(str(output_path))
    return True, None


def main():
    parser = argparse.ArgumentParser(description="Convert Beamer PDF to PPTX")
    parser.add_argument("--input", "-i", required=True, help="Input PDF path")
    parser.add_argument("--output", "-o", default=None, help="Output PPTX path")
    parser.add_argument("--engine", "-e", default="auto",
                        choices=["auto", "wps", "wps-basic", "pymupdf"],
                        help="Conversion engine (default: auto = WPS first, PyMuPDF fallback)")
    parser.add_argument("--dpi", "-d", type=int, default=300,
                        help="PyMuPDF render DPI (only for pymupdf engine, default: 300)")
    args = parser.parse_args()

    pdf_path = Path(args.input)
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else pdf_path.with_suffix(".pptx")

    print(f"Converting: {pdf_path.name}")

    success = False
    used_engine = ""

    if args.engine in ("auto", "wps"):
        # Try AI engine first, then basic
        for eng in (["ai"] if args.engine == "wps" else ["ai", "basic"]):
            ok, err = convert_wps(pdf_path, output_path, engine=eng)
            if ok:
                success = True
                used_engine = f"WPS ({eng})"
                break
            elif args.engine == "wps":
                print(f"  WPS failed: {err}", file=sys.stderr)
                sys.exit(1)
            # auto mode: try next engine

    if args.engine == "wps-basic":
        ok, err = convert_wps(pdf_path, output_path, engine="basic")
        if ok:
            success = True
            used_engine = "WPS (basic)"
        else:
            print(f"  WPS basic failed: {err}", file=sys.stderr)
            sys.exit(1)

    if not success and args.engine in ("auto", "pymupdf"):
        ok, err = convert_pymupdf(pdf_path, output_path, dpi=args.dpi)
        if ok:
            success = True
            used_engine = "PyMuPDF (image)"
        else:
            print(f"  PyMuPDF failed: {err}", file=sys.stderr)
            sys.exit(1)

    if not success:
        print("Error: All conversion engines failed", file=sys.stderr)
        sys.exit(1)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\nDone: {output_path}")
    print(f"  Engine: {used_engine}, Size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
