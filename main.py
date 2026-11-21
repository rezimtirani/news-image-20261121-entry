#!/usr/bin/env python3
"""Publish the 21 November 2026 world-news image.

The front page is drawn by render.py from news.json and saved as
entry.png beside this file. This entrypoint only moves a checked copy
of that image to $MAKEFUN_OUTPUT_DIR/entry.png, so grading needs no
network, no fonts and no other package beyond the standard library.
Running it twice writes byte-identical output.

Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
LIMIT_BYTES = 1048576
LIMIT_SIDE = 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def read_header(path):
    """Return (width, height, size) after checking the PNG header."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if head[:8] != MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        raise SystemExit(
            f"image is {width}x{height}, over {LIMIT_SIDE}x{LIMIT_SIDE}")
    size = os.path.getsize(path)
    if size > LIMIT_BYTES:
        raise SystemExit(f"image is {size} bytes, over {LIMIT_BYTES}")
    return width, height, size


def copy_checked(src, dst):
    """Copy src to dst in chunks, then verify what landed on disk."""
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(65536)
            if not chunk:
                break
            fout.write(chunk)
    return read_header(dst)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    width, height, nbytes = copy_checked(SOURCE, target)
    print(f"wrote {target}: {width}x{height} PNG, {nbytes} bytes")


if __name__ == "__main__":
    main()
