#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

The day's stories live in news.json, researched from AP, Reuters, NPR
and TradingView wires of 21 November 2026. Everything runs offline and
deterministically: the same news.json always produces the same entry.png.

Usage: python3 render.py
"""
import json, math, os

from PIL import Image
from PIL import ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PALETTE = {
    "ink": (24, 30, 38),
    "paper": (248, 244, 235),
    "navy": (13, 40, 68),
    "navy_soft": (203, 214, 226),
    "gold": (198, 158, 36),
    "gold_pale": (233, 197, 94),
    "card": (255, 255, 255),
    "grey": (86, 96, 108),
    "rule": (212, 204, 188),
    "red": (164, 27, 27),
    "teal": (14, 116, 108),
    "blue": (28, 76, 148),
    "green": (45, 122, 48),
}
PAGE = (1024, 1024)
MASTHEAD_H = 140
HERO_TOP, HERO_BOTTOM = 158, 424
GRID_TOP, GRID_ROW_H = 434, 194
BRIEFS_Y = 814
FOOTER_TOP = 954


class FrontPage:
    """A newspaper front page drawn onto a Pillow image."""

    def __init__(self, data):
        self.data = data
        self.img = Image.new("RGB", PAGE, PALETTE["paper"])
        self.d = ImageDraw.Draw(self.img)

    def c(self, name):
        return PALETTE[name]

    def typeface(self, bold, size):
        fname = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(os.path.join(FONT_DIR, fname), size)

    def wrap(self, text, fnt, width):
        """Greedy word wrap of text to the given pixel width."""
        out, cur = [], ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if self.d.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = word
        if cur:
            out.append(cur)
        return out

    def lines(self, x, y, items, fnt, colour, gap):
        """Draw lines top to bottom; return the y just below the last."""
        for item in items:
            self.d.text((x, y), item, font=fnt, fill=colour)
            y += gap
        return y

    def card(self, box):
        self.d.rounded_rectangle(box, radius=10, fill=self.c("card"),
                                 outline=self.c("rule"), width=2)

    def burst(self, box, colour):
        """Explosion burst: spikes radiating from a hot core."""
        x, y, w, h = box
        cx, cy = x + w // 2, y + h // 2
        for step in range(12):
            ang = math.radians(step * 30)
            near = 18 if step % 2 == 0 else 30
            far = 52 if step % 2 == 0 else 66
            self.d.line([cx + near * math.cos(ang), cy + near * math.sin(ang),
                         cx + far * math.cos(ang), cy + far * math.sin(ang)],
                        fill=colour, width=6)
        self.d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=colour)
        self.d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9],
                       fill=(255, 255, 255))

    def market_chart(self, box, colour):
        """Falling market chart: axes and a line diving down."""
        x, y, w, h = box
        self.d.line([x + 10, y + 12, x + 10, y + h - 12], fill=colour,
                    width=5)
        self.d.line([x + 10, y + h - 12, x + w - 8, y + h - 12],
                    fill=colour, width=5)
        pts = [(x + 16, y + 26), (x + 34, y + 34), (x + 50, y + 30),
               (x + 66, y + 52), (x + 80, y + 74)]
        self.d.line(pts, fill=colour, width=6, joint="curve")
        self.d.polygon([(x + 80, y + 74), (x + 68, y + 70), (x + 78, y + 88)],
                       fill=colour)

    def dialogue(self, box, colour):
        """Two speech bubbles facing each other: negotiations."""
        x, y, w, h = box
        self.d.rounded_rectangle([x + 4, y + 10, x + w // 2 + 8,
                                  y + h // 2 + 6], radius=12,
                                 outline=colour, width=5)
        self.d.polygon([(x + 18, y + h // 2 + 6), (x + 34, y + h // 2 + 6),
                        (x + 20, y + h // 2 + 24)], fill=colour)
        self.d.rounded_rectangle([x + w // 2 - 8, y + h // 2 - 2, x + w - 4,
                                  y + h - 10], radius=12, outline=colour,
                                 width=5)
        self.d.polygon([(x + w - 34, y + h - 10), (x + w - 18, y + h - 10),
                        (x + w - 20, y + h - 10 + 18)], fill=colour)

    def shield(self, box, colour):
        """Shield with a lock: a cyberattack repelled."""
        x, y, w, h = box
        cx = x + w // 2
        top = y + 8
        self.d.polygon([(cx - 34, top), (cx + 34, top), (cx + 34, top + 34),
                        (cx, top + 76), (cx - 34, top + 34)],
                       outline=colour, width=5)
        self.d.ellipse([cx - 11, top + 30, cx + 11, top + 52],
                       outline=colour, width=5)
        self.d.line([cx, top + 48, cx, top + 62], fill=colour, width=5)

    def world(self, box, colour):
        """Globe: climate talks for the whole planet."""
        x, y, w, h = box
        cx, cy = x + w // 2, y + h // 2
        r = min(w, h) // 2 - 6
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour,
                       width=5)
        self.d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                       outline=colour, width=4)
        self.d.line([cx - r, cy, cx + r, cy], fill=colour, width=4)
        self.d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
                   fill=colour, width=4)

    def masthead(self):
        self.d.rectangle([0, 0, PAGE[0], MASTHEAD_H], fill=self.c("navy"))
        self.d.rectangle([0, MASTHEAD_H, PAGE[0], MASTHEAD_H + 6],
                         fill=self.c("gold"))
        self.d.text((28, 20), self.data["title"],
                    font=self.typeface(True, 64), fill=(255, 255, 255))
        self.d.text((30, 100), self.data["subtitle"],
                    font=self.typeface(False, 23), fill=self.c("navy_soft"))
        self.d.text((996, 22), self.data["weekday"],
                    font=self.typeface(True, 28), fill=self.c("gold_pale"),
                    anchor="ra")
        self.d.text((996, 56), self.data["dateline"],
                    font=self.typeface(True, 38), fill=(255, 255, 255),
                    anchor="ra")

    def hero(self):
        story = self.data["hero"]
        self.card([24, HERO_TOP, 1000, HERO_BOTTOM])
        self.d.rounded_rectangle([24, HERO_TOP, 244, HERO_BOTTOM], radius=10,
                                 fill=self.c("red"))
        self.d.rectangle([200, HERO_TOP, 244, HERO_BOTTOM],
                         fill=self.c("red"))
        self.burst((44, 208, 176, 140), (255, 255, 255))
        self.d.text((268, 176), story["kicker"],
                    font=self.typeface(True, 21), fill=self.c("red"))
        y = self.lines(268, 204,
                       self.wrap(story["headline"], self.typeface(True, 42),
                                 700),
                       self.typeface(True, 42), self.c("navy"), 50)
        self.lines(268, y + 12,
                   self.wrap(story["body"], self.typeface(False, 25), 700),
                   self.typeface(False, 25), self.c("grey"), 33)

    def story_grid(self):
        glyphs = [self.market_chart, self.dialogue, self.shield, self.world]
        accents = ["red", "blue", "teal", "green"]
        for i, story in enumerate(self.data["stories"]):
            col, row = i % 2, i // 2
            x0 = 24 + col * 504
            y0 = GRID_TOP + row * GRID_ROW_H
            self.card([x0, y0, x0 + 472, y0 + 180])
            self.d.rectangle([x0 + 10, y0, x0 + 462, y0 + 8],
                             fill=self.c(accents[i]))
            glyphs[i]((x0 + 14, y0 + 42, 84, 92), self.c(accents[i]))
            tx = x0 + 110
            self.d.text((tx, y0 + 24), story["kicker"],
                        font=self.typeface(True, 19),
                        fill=self.c(accents[i]))
            y = self.lines(tx, y0 + 50,
                           self.wrap(story["headline"],
                                     self.typeface(True, 28), 346)[:2],
                           self.typeface(True, 28), self.c("ink"), 34)
            self.lines(tx, y + 6,
                       self.wrap(story["body"], self.typeface(False, 18),
                                 346)[:2],
                       self.typeface(False, 18), self.c("grey"), 24)

    def also_today(self):
        self.d.text((28, BRIEFS_Y), "ALSO TODAY",
                    font=self.typeface(True, 22), fill=self.c("navy"))
        self.d.line([170, BRIEFS_Y + 14, 996, BRIEFS_Y + 14],
                    fill=self.c("rule"), width=2)
        for i, brief in enumerate(self.data["briefs"]):
            bx = 28 + i * 247
            self.d.rectangle([bx, 856, bx + 14, 870], fill=self.c("navy"))
            self.lines(bx + 24, 850,
                       self.wrap(brief["headline"], self.typeface(True, 20),
                                 210)[:2],
                       self.typeface(True, 20), self.c("ink"), 25)
            self.lines(bx + 24, 904,
                       self.wrap(brief["body"], self.typeface(False, 17),
                                 210)[:2],
                       self.typeface(False, 17), self.c("grey"), 22)

    def footer(self):
        self.d.rectangle([0, FOOTER_TOP, PAGE[0], FOOTER_TOP + 38],
                         fill=self.c("red"))
        self.d.text((512, FOOTER_TOP + 10), self.data["ticker"],
                    font=self.typeface(True, 20), fill=(255, 255, 255),
                    anchor="ma")
        self.d.text((512, 998), self.data["sources"],
                    font=self.typeface(False, 14), fill=self.c("grey"),
                    anchor="ma")

    def build(self):
        self.masthead()
        self.hero()
        self.story_grid()
        self.also_today()
        self.footer()
        return self.img


def main():
    with open(os.path.join(ROOT, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    page = FrontPage(data)
    image = page.build()
    out = os.path.join(ROOT, "entry.png")
    image.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    if size > 1_048_576:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB cap")
    print("wrote", out, image.size, size, "bytes")


if __name__ == "__main__":
    main()
