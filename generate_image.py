#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024).

Fresh code written for the news-image-20261124 make.fun bounty.
Pictogram-style illustrations only; no photos, no network.
"""
import math
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (24, 24, 24)
RED = (176, 30, 36)
BLUE = (31, 78, 140)
GREEN = (34, 120, 64)
GOLD = (201, 148, 32)
GREY = (90, 88, 82)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)         # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)           # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 6
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------- pictograms (simple geometric drawings) ----------

def pic_climate(d, cx, cy, r):
    # Globe: blue circle, green land blobs, red sun, grey smoke.
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 170, 210),
              outline=INK, width=3)
    d.ellipse([cx - r * 0.7, cy - r * 0.55, cx - r * 0.1, cy - r * 0.05],
              fill=GREEN)
    d.ellipse([cx + r * 0.05, cy + r * 0.1, cx + r * 0.65, cy + r * 0.6],
              fill=GREEN)
    d.arc([cx - r, cy - r * 0.35, cx + r, cy + r * 0.35], 0, 180, fill=INK,
          width=2)
    d.ellipse([cx + r * 0.55, cy - r * 1.25, cx + r * 1.05, cy - r * 0.75],
              fill=RED)
    for i, yy in enumerate((-r * 1.05, -r * 0.85)):
        d.line([cx + r * 0.15 + i * 8, cy + yy, cx + r * 0.55 + i * 8,
                cy + yy - 14], fill=GREY, width=4)


def pic_dove(d, cx, cy, r):
    # Olive branch: diagonal stem with green leaves.
    d.line([cx - r * 0.8, cy + r * 0.8, cx + r * 0.8, cy - r * 0.8],
           fill=GREEN, width=5)
    for t in (0.2, 0.45, 0.7):
        x = cx - r * 0.8 + t * r * 1.6
        y = cy + r * 0.8 - t * r * 1.6
        d.ellipse([x - 22, y - 34, x + 2, y - 6], fill=GREEN,
                  outline=INK, width=2)
        d.ellipse([x - 2, y + 6, x + 22, y + 34], fill=GREEN,
                  outline=INK, width=2)
    d.ellipse([cx + r * 0.55, cy - r * 0.95, cx + r * 0.95, cy - r * 0.55],
              fill=INK)
    d.ellipse([cx + r * 0.35, cy - r * 0.75, cx + r * 0.75, cy - r * 0.35],
              fill=INK)


def pic_ship(d, cx, cy, r):
    # Ship on waves under a blue-yellow sky band.
    d.rectangle([cx - r, cy - r, cx + r, cy - r * 0.25], fill=(66, 135, 200))
    d.rectangle([cx - r, cy - r * 0.25, cx + r, cy], fill=(252, 209, 42))
    d.polygon([(cx - r * 0.8, cy + r * 0.1), (cx + r * 0.8, cy + r * 0.1),
               (cx + r * 0.55, cy + r * 0.55), (cx - r * 0.55, cy + r * 0.55)],
              fill=INK)
    d.rectangle([cx - r * 0.25, cy - r * 0.35, cx + r * 0.25, cy + r * 0.1],
                fill=INK)
    for k in range(3):
        yy = cy + r * 0.72 + k * 12
        d.arc([cx - r + k * 14, yy - 8, cx - r * 0.2 + k * 14, yy + 8],
              180, 360, fill=BLUE, width=3)
        d.arc([cx + k * 14, yy - 8, cx + r * 0.8 + k * 14, yy + 8],
              180, 360, fill=BLUE, width=3)


def pic_scales(d, cx, cy, r):
    # Scales of justice.
    d.line([cx, cy - r, cx, cy + r * 0.8], fill=INK, width=5)
    d.line([cx - r * 0.85, cy - r * 0.55, cx + r * 0.85, cy - r * 0.55],
           fill=INK, width=5)
    d.ellipse([cx - 7, cy - r - 9, cx + 7, cy - r + 5], fill=GOLD,
              outline=INK, width=2)
    for sx in (-r * 0.85, r * 0.85):
        d.line([cx + sx, cy - r * 0.55, cx + sx, cy - r * 0.05], fill=INK,
               width=3)
        d.arc([cx + sx - 26, cy - r * 0.05, cx + sx + 26, cy + r * 0.45],
              0, 180, fill=GOLD, width=4)
    d.rectangle([cx - r * 0.5, cy + r * 0.8, cx + r * 0.5, cy + r * 0.95],
                fill=INK)


def pic_chart(d, cx, cy, r):
    # Rising market bars with an arrow.
    bars = [0.25, 0.4, 0.35, 0.6, 0.8, 1.0]
    bw = int(r * 1.7 / len(bars))
    for i, frac in enumerate(bars):
        x0 = cx - r + i * bw + 3
        bh = int(r * 1.1 * frac)
        d.rectangle([x0, cy + r * 0.6 - bh, x0 + bw - 6, cy + r * 0.6],
                    fill=GREEN)
    pts = [(cx - r + i * bw + bw // 2, cy + r * 0.6 - int(r * 1.1 * f) - 8)
           for i, f in enumerate(bars)]
    d.line(pts, fill=RED, width=4)
    ex, ey = pts[-1]
    d.polygon([(ex, ey - 16), (ex + 18, ey + 2), (ex - 2, ey + 6)], fill=RED)
    d.line([cx - r, cy + r * 0.6, cx + r, cy + r * 0.6], fill=INK, width=3)


def pic_cross(d, cx, cy, r):
    # Medical cross in a circle, with small virus dots.
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=RED, width=4)
    d.rectangle([cx - 12, cy - r * 0.55, cx + 12, cy + r * 0.55], fill=RED)
    d.rectangle([cx - r * 0.55, cy - 12, cx + r * 0.55, cy + 12], fill=RED)
    for ang in (30, 150, 250):
        a = math.radians(ang)
        x = cx + int(r * 1.15 * math.cos(a))
        y = cy + int(r * 1.15 * math.sin(a))
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=INK)


# ---------- page ----------

def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)

    # Top line
    d.text((36, 26), "WORLD NEWS  •  ONE DAY, ONE PAGE",
           font=SANS_B(19), fill=GREY)
    right_txt = "No. 328  •  PRICE: FREE"
    d.text((1024 - 36 - d.textlength(right_txt, font=SANS(19)), 26),
           right_txt, font=SANS(19), fill=GREY)
    d.line([36, 56, W - 36, 56], fill=INK, width=2)

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 66), title, font=tf,
           fill=INK)
    sub = "—  THE DAY'S NEWS, SUMMED UP IN A SINGLE PICTURE  —"
    sf = SANS(20)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 138), sub, font=sf,
           fill=GREY)

    # Date banner
    d.rectangle([36, 168, W - 36, 216], fill=RED)
    date = "TUESDAY 24 NOVEMBER 2026"
    df = SANS_B(38)
    d.text(((W - d.textlength(date, font=df)) / 2, 176), date, font=df,
           fill=(255, 255, 255))

    # ---- Lead story: COP31 ----
    y = 232
    d.text((36, y), "CLIMATE  •  ANTALYA, TURKEY", font=SANS_B(20), fill=RED)
    y += 28
    head = "CLIMATE SUMMIT ENDS WITH NO DEAL"
    hf = SERIF_B(42)
    y = draw_lines(d, wrap(d, head, hf, 600), 36, y, hf, leading=48)
    y += 6
    lead = ("COP31 in Antalya ends without a deal — the first UN climate "
            "summit since Copenhagen (2009) to fail. Talks split over "
            "fossil fuels and finance.")
    y = draw_lines(d, wrap(d, lead, SANS(23), 600), 36, y, SANS(23),
                   leading=30)
    pic_climate(d, 830, 320, 78)

    d.line([36, 458, W - 36, 458], fill=INK, width=2)

    # ---- Grid of four stories ----
    cols = [36, 532]
    col_w = 456
    rows = [474, 660]
    row_h = 172
    stories = [
        ("GAZA", "GAZA STRIKE KILLS HAMAS CHIEF",
         "Israeli strikes kill Hamas security chief Naeem Abu Nahel and six "
         "others in Gaza City.",
         pic_dove),
        ("UKRAINE  •  LIBYA", "UKRAINE WAR SPILLS INTO LIBYA WATERS",
         "Kyiv confirms drone strikes on Russian ships off Libya as "
         "self-defence; 2 die in Zaporizhzhia.",
         pic_ship),
        ("LAW  •  MYANMAR", "14 NATIONS BACK ROHINGYA RULING",
         "Fourteen nations back the court ruling that Myanmar committed "
         "genocide against the Rohingya.",
         pic_scales),
        ("MARKETS  •  TECH", "STOCKS SOAR AS HUANG RETURNS",
         "Jensen Huang returns as Nvidia CEO after Trump's intervention; "
         "the Nasdaq jumps 6.5%.",
         pic_chart),
    ]
    for i, (kick, headline, summary, pic) in enumerate(stories):
        x = cols[i % 2]
        yy = rows[i // 2]
        d.text((x, yy), kick, font=SANS_B(18), fill=RED)
        hy = yy + 26
        lines = wrap(d, headline, SERIF_B(26), col_w - 96)
        hy = draw_lines(d, lines, x, hy, SERIF_B(26), leading=30)
        sy = hy + 4
        draw_lines(d, wrap(d, summary, SANS(19), col_w), x, sy,
                   SANS(19), leading=24)
        pic(d, x + col_w - 40, yy + 40, 36)
        if i % 2 == 0:
            d.line([512, yy, 512, yy + row_h - 8], fill=(190, 184, 170),
                   width=1)
    d.line([36, 648, W - 36, 648], fill=(190, 184, 170), width=1)

    # ---- Bottom band: Congo Ebola ----
    d.line([36, 844, W - 36, 844], fill=INK, width=2)
    y = 856
    d.text((150, y), "HEALTH  •  DR CONGO", font=SANS_B(18), fill=RED)
    d.text((150, y + 24), "FIGHTING TRAPS EBOLA TEAMS IN CONGO",
           font=SERIF_B(27), fill=INK)
    draw_lines(d, wrap(d, "Fighting in Ituri forces Ebola responders to take "
                    "cover, the WHO says.",
                    SANS(20), 838), 150, y + 58, SANS(20), leading=25)
    pic_cross(d, 92, 912, 38)

    # ---- Footer ticker ----
    d.line([36, 958, W - 36, 958], fill=INK, width=2)
    tick = ("ALSO ON 24 NOVEMBER:  US states sue SpaceX over Grok images  •  "
            "5.6 quake hits Nepal")
    tf2 = SANS(17)
    d.text((36, 972), tick, font=tf2, fill=GREY)

    img.save(path, "PNG", optimize=True)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")
