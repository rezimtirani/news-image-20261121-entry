#!/usr/bin/env python3
"""Render the Saturday 21 November 2026 world-news front page.

The stories in news.json were researched from AP, Reuters, NPR and
TradingView reporting of 21 November 2026 (morning editions and
overnight wires). This script draws them as a 1024x1024 newspaper
front page, entry.png. It runs fully offline and is deterministic:
the same news.json always yields the same PNG bytes.

Run it with: python3 render.py
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
INK = (24, 30, 38)
PAPER = (248, 244, 235)
NAVY = (13, 40, 68)
NAVY_SOFT = (203, 214, 226)
GOLD = (198, 158, 36)
GOLD_PALE = (233, 197, 94)
CARD = (255, 255, 255)
GREY = (86, 96, 108)
RULE = (212, 204, 188)
RED = (164, 27, 27)
TEAL = (14, 116, 108)
BLUE = (28, 76, 148)
GREEN = (45, 122, 48)
PLUM = (104, 60, 154)


def font(weight, size):
    name = "DejaVuSans-Bold.ttf" if weight == "bold" else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap of text to the given pixel width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, fnt, colour, step):
    """Draw lines top to bottom; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=colour)
        y += step
    return y


def panel(draw, box, fill=CARD, edge=RULE):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=edge, width=2)


def burst_glyph(draw, x, y, w, h, colour):
    """An explosion burst: radiating spikes around a hot core."""
    cx, cy = x + w // 2, y + h // 2
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        r1 = 18 if angle % 60 == 0 else 30
        r2 = 52 if angle % 60 == 0 else 66
        draw.line([cx + int(r1 * math.cos(rad)), cy + int(r1 * math.sin(rad)),
                   cx + int(r2 * math.cos(rad)), cy + int(r2 * math.sin(rad))],
                  fill=colour, width=6)
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=colour)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 255, 255))


def chart_glyph(draw, x, y, w, h, colour):
    """A falling market chart: axes and a line diving down."""
    draw.line([x + 10, y + 12, x + 10, y + h - 12], fill=colour, width=5)
    draw.line([x + 10, y + h - 12, x + w - 8, y + h - 12], fill=colour, width=5)
    pts = [(x + 16, y + 26), (x + 34, y + 34), (x + 50, y + 30),
           (x + 66, y + 52), (x + 80, y + 74)]
    draw.line(pts, fill=colour, width=6, joint="curve")
    draw.polygon([(x + 80, y + 74), (x + 68, y + 70), (x + 78, y + 88)],
                 fill=colour)


def talks_glyph(draw, x, y, w, h, colour):
    """Two speech bubbles facing each other: negotiations."""
    draw.rounded_rectangle([x + 4, y + 10, x + w // 2 + 8, y + h // 2 + 6],
                           radius=12, outline=colour, width=5)
    draw.polygon([(x + 18, y + h // 2 + 6), (x + 34, y + h // 2 + 6),
                  (x + 20, y + h // 2 + 24)], fill=colour)
    draw.rounded_rectangle([x + w // 2 - 8, y + h // 2 - 2, x + w - 4,
                            y + h - 10], radius=12, outline=colour, width=5)
    draw.polygon([(x + w - 34, y + h - 10), (x + w - 18, y + h - 10),
                  (x + w - 20, y + h - 10 + 18)], fill=colour)


def shield_glyph(draw, x, y, w, h, colour):
    """A shield with a lock: a cyberattack repelled."""
    cx = x + w // 2
    top = y + 8
    draw.polygon([(cx - 34, top), (cx + 34, top), (cx + 34, top + 34),
                  (cx, top + 76), (cx - 34, top + 34)], outline=colour, width=5)
    draw.ellipse([cx - 11, top + 30, cx + 11, top + 52], outline=colour,
                 width=5)
    draw.line([cx, top + 48, cx, top + 62], fill=colour, width=5)


def globe_glyph(draw, x, y, w, h, colour):
    """A globe: climate talks for the whole planet."""
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 6
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=5)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=colour, width=4)
    draw.line([cx - r, cy, cx + r, cy], fill=colour, width=4)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
             fill=colour, width=4)


GLYPHS = [chart_glyph, talks_glyph, shield_glyph, globe_glyph]
ACCENTS = [RED, BLUE, TEAL, GREEN]


def masthead(draw, data):
    draw.rectangle([0, 0, W, 140], fill=NAVY)
    draw.rectangle([0, 140, W, 146], fill=GOLD)
    draw.text((28, 20), data["title"], font=font("bold", 64), fill=(255, 255, 255))
    draw.text((30, 100), data["subtitle"], font=font("regular", 23), fill=NAVY_SOFT)
    draw.text((996, 22), data["weekday"], font=font("bold", 28),
              fill=GOLD_PALE, anchor="ra")
    draw.text((996, 56), data["dateline"], font=font("bold", 38),
              fill=(255, 255, 255), anchor="ra")


def hero(draw, data):
    story = data["hero"]
    panel(draw, [24, 158, 1000, 424])
    draw.rounded_rectangle([24, 158, 244, 424], radius=10, fill=RED)
    draw.rectangle([200, 158, 244, 424], fill=RED)
    burst_glyph(draw, 44, 208, 176, 140, (255, 255, 255))
    draw.text((268, 176), story["kicker"], font=font("bold", 21), fill=RED)
    y = text_block(draw, 268, 204,
                   fit_lines(draw, story["headline"], font("bold", 42), 700),
                   font("bold", 42), NAVY, 50)
    text_block(draw, 268, y + 12,
               fit_lines(draw, story["body"], font("regular", 25), 700),
               font("regular", 25), GREY, 33)


def story_grid(draw, data):
    for i, story in enumerate(data["stories"]):
        col, row = i % 2, i // 2
        x0 = 24 + col * 504
        y0 = 434 + row * 194
        panel(draw, [x0, y0, x0 + 472, y0 + 180])
        draw.rectangle([x0 + 10, y0, x0 + 462, y0 + 8], fill=ACCENTS[i])
        GLYPHS[i](draw, x0 + 14, y0 + 42, 84, 92, ACCENTS[i])
        tx = x0 + 110
        draw.text((tx, y0 + 24), story["kicker"], font=font("bold", 19),
                  fill=ACCENTS[i])
        y = text_block(draw, tx, y0 + 50,
                       fit_lines(draw, story["headline"], font("bold", 28), 346)[:2],
                       font("bold", 28), INK, 34)
        text_block(draw, tx, y + 6,
                   fit_lines(draw, story["body"], font("regular", 18), 346)[:2],
                   font("regular", 18), GREY, 24)


def briefs(draw, data):
    draw.text((28, 814), "ALSO TODAY", font=font("bold", 22), fill=NAVY)
    draw.line([170, 828, 996, 828], fill=RULE, width=2)
    for i, brief in enumerate(data["briefs"]):
        bx = 28 + i * 247
        draw.rectangle([bx, 856, bx + 14, 870], fill=NAVY)
        text_block(draw, bx + 24, 850,
                   fit_lines(draw, brief["headline"], font("bold", 20), 210)[:2],
                   font("bold", 20), INK, 25)
        text_block(draw, bx + 24, 904,
                   fit_lines(draw, brief["body"], font("regular", 17), 210)[:2],
                   font("regular", 17), GREY, 22)


def footer(draw, data):
    draw.rectangle([0, 954, W, 992], fill=RED)
    draw.text((512, 964), data["ticker"], font=font("bold", 20),
              fill=(255, 255, 255), anchor="ma")
    draw.text((512, 998), data["sources"], font=font("regular", 14),
              fill=GREY, anchor="ma")


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    masthead(draw, data)
    hero(draw, data)
    story_grid(draw, data)
    briefs(draw, data)
    footer(draw, data)
    out = os.path.join(HERE, "entry.png")
    image.save(out, format="PNG", optimize=True)
    print("wrote", out, image.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
