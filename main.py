#!/usr/bin/env python3
"""Ship the 21 November 2026 front page as the competition entry.

render.py draws entry.png from news.json. This script is the entrypoint:
it copies that image, after checking it, into $MAKEFUN_OUTPUT_DIR.
Only the standard library is used, there is no network, and running it
twice writes identical bytes.

Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os, struct

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "entry.png")
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def inspect_png(path):
    """Check the PNG header and size; return (width, height, bytes)."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != PNG_SIG:
        raise SystemExit("not a PNG file: " + path)
    if head[12:16] != b"IHDR":
        raise SystemExit("PNG has no IHDR chunk: " + path)
    w, h = struct.unpack(">II", head[16:24])
    if w > MAX_SIDE or h > MAX_SIDE:
        raise SystemExit(f"image is {w}x{h}, limit is {MAX_SIDE}x{MAX_SIDE}")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(f"image is {size} bytes, limit is {MAX_BYTES}")
    return w, h, size


def copy_png(src, dst):
    """Copy src to dst in chunks, then verify what landed on disk."""
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(65536)
            if not chunk:
                break
            fout.write(chunk)
    return inspect_png(dst)


def run():
    if not os.path.exists(SRC):
        raise SystemExit("entry.png is missing; run render.py first: " + SRC)
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, "entry.png")
    w, h, n = copy_png(SRC, dest)
    print(f"wrote {dest}: {w}x{h} PNG, {n} bytes")


if __name__ == "__main__":
    run()
