#!/usr/bin/env python3
"""THE WORLD TODAY - Friday 20 November 2026.

Draws a dense newspaper front page summing up the world's news of
Friday 20 November 2026, as a 1024x1024 PNG.

Pure Python stdlib + Pillow, no network, fully deterministic:
no randomness, no clocks, no timestamps. Two runs produce
byte-identical output.

Layout: masthead, lead story with a drawn Kyiv-bridges panel,
four columns of short headline-only stories, a strip of three
drawn illustration panels, a DAY IN NUMBERS strip, footer.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
GAP = 12
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (60, 58, 52)
PANEL = (238, 232, 218)
PANEL_LINE = (180, 172, 156)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)             # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- stories
# Every story below happened or was first reported on Friday 20 Nov 2026.
# Headlines are self-contained: each carries the key fact.
# Regions: EUROPE / MARKETS / TECH / ASIA-PACIFIC / MIDDLE EAST / AMERICAS
#          / CLIMATE & SCIENCE
STORIES = [
    ("EUROPE", "Two Russian missiles land in Poland — Lublin and Subcarpathian, no casualties"),
    ("EUROPE", "Hungary lifts veto on opening EU accession talks with Ukraine"),
    ("EUROPE", "Ukraine, Germany, France and UK agree legally binding security guarantees"),
    ("EUROPE", "Operation Bear Trap: Ukraine retakes 14 settlements in Kharkiv"),
    ("EUROPE", "EU to summon Russian ambassador over the overnight Kyiv strikes"),
    ("EUROPE", "Zelensky: NATO membership is the strongest security guarantee"),
    ("MARKETS", "AI rout: S&P 500 falls 3.7% to 6,910.39, into correction"),
    ("MARKETS", "Nasdaq down 5.3%, now negative for 2026; Dow drops 950 points"),
    ("MARKETS", "Nvidia sinks 14%; Anthropic falls 9% a day after its record IPO"),
    ("MARKETS", "SEC reviews potential accounting issues at Nvidia"),
    ("TECH", "Trump weighs forcing US firms to disclose use of Chinese-made AI"),
    ("TECH", "Musk calls $500m US election spending 'pretty foolish'"),
    ("TECH", "US defence chair rejects the Pentagon's $350bn budget request"),
    ("ASIA-PACIFIC", "Trump: penalties for US firms building AI data centres abroad"),
    ("ASIA-PACIFIC", "China limited to older-generation AI chips, including the H200"),
    ("ASIA-PACIFIC", "US and China agree humans must oversee military AI decisions"),
    ("ASIA-PACIFIC", "China bars a Bloomberg reporter from the trilateral summit"),
    ("ASIA-PACIFIC", "Xi hails 'full reversal' in ties after meeting Albanese"),
    ("ASIA-PACIFIC", "NZ court: pay-equity reform breached women's rights"),
    ("MIDDLE EAST", "Saudi-led coalition intercepts Houthi missile aimed at Riyadh"),
    ("MIDDLE EAST", "US pulls carrier USS George Washington from the Persian Gulf"),
    ("MIDDLE EAST", "US blockade of Iran goes on; Trump claims control of Hormuz"),
    ("MIDDLE EAST", "16 Arab and Islamic states welcome UK and Australia steps on Israel"),
    ("MIDDLE EAST", "West presses Iran at IAEA to allow inspections of struck nuclear sites"),
    ("MIDDLE EAST", "Iraq: fresh airstrikes expose security threat as US troops draw down"),
    ("AMERICAS", "US embassy: Chinese chemicals fuel the Sinaloa cartel"),
    ("AMERICAS", "Global car-smuggling raids: 2,393 seizures, 688 arrests"),
    ("AMERICAS", "Colombia president warns against state intervention over blockade"),
    ("AMERICAS", "Pancreatic cancer pill: tumour undetectable in 1 of 12 patients"),
    ("CLIMATE & SCIENCE", "COP31 deadlocked on fossil fuels; draft drops all mention, talks overtime"),
    ("CLIMATE & SCIENCE", "COP31: India pushes a country-based just transition"),
    ("CLIMATE & SCIENCE", "Peru quake M6.7 shakes Junin, felt in Lima; no deaths"),
    ("CLIMATE & SCIENCE", "Myanmar rejects Rohingya genocide ruling as 'unfair'"),
    ("CLIMATE & SCIENCE", "UN Assembly chief visits Cox's Bazar camps a day after ICJ verdict"),
    ("CLIMATE & SCIENCE", "Turkey urges bloc to shield auto market access under 'Made in EU'"),
]

LEAD_HEADLINE = "Russia rains 400+ drones and 110 missiles on Kyiv"
LEAD_SUMMARY = ("Overnight barrage hits three Dnipro bridges; eight killed, about "
                "thirty wounded. Two missiles fall in Poland. Europe vows a "
                "response as Ukraine retakes ground in Kharkiv.")

NUMBERS = [
    ("400+", "drones fired at Kyiv"),
    ("110", "missiles in the barrage"),
    ("-3.7%", "S&P 500 in one day"),
    ("M6.7", "quake in Peru"),
    ("2,393", "cars seized in raids"),
    ("1 in 12", "tumours undetectable"),
]


# ---------------------------------------------------------------- drawing
def draw_masthead(d, y):
    d.text((W // 2, y), "THE WORLD TODAY", font=F_SERIF(52),
           fill=INK, anchor="ma")
    y += 68
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=3)
    y += 9
    d.text((W // 2, y), "FRIDAY 20 NOVEMBER 2026", font=F_BOLD(28),
           fill=RED, anchor="ma")
    y += 38
    d.text((W // 2, y),
           "35 stories  ·  date-checked  ·  seven regions  ·  one day's news",
           font=F_SANS(14), fill=GREY, anchor="ma")
    y += 24
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=3)
    return y + 9


def draw_bridges(d, x, y, w, h):
    """Kyiv: river, three Dnipro bridges, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238),
                outline=PANEL_LINE, width=1)
    d.text((x + 8, y + 6), "THE OVERNIGHT BARRAGE", font=F_BOLD(10),
           fill=GREY)
    # smoke puffs, kept clear of the label at top-left
    for sx, sy, sr in [(x + 205, y + 15, 10), (x + 219, y + 8, 7),
                       (x + 243, y + 17, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 148, 142))
    # river
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 158, 196))
    # bridges
    for bx in (x + 30, x + 105, x + 180):
        d.line([(bx, y + h - 34), (bx + 60, y + h - 34)], fill=INK, width=4)
        d.line([(bx + 8, y + h - 34), (bx + 30, y + h - 62),
                (bx + 52, y + h - 34)], fill=INK, width=2)
        d.line([(bx + 30, y + h - 62), (bx + 30, y + h - 34)], fill=INK, width=2)
    d.text((x + 8, y + h - 20), "KYIV: THREE BRIDGES HIT",
           font=F_BOLD(11), fill=(255, 255, 255))


def draw_lead(d, y):
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 9
    txt_w = 640
    d.text((MARGIN, y), "LEAD  ·  EUROPE", font=F_BOLD(12), fill=RED)
    y += 19
    for ln in wrap(d, LEAD_HEADLINE, F_BOLD(26), txt_w):
        d.text((MARGIN, y), ln, font=F_BOLD(26), fill=INK)
        y += 31
    y += 3
    for ln in wrap(d, LEAD_SUMMARY, F_SANS(13), txt_w):
        d.text((MARGIN, y), ln, font=F_SANS(13), fill=INK)
        y += 18
    draw_bridges(d, W - MARGIN - 300, y - 104, 300, 104)
    return y + 12


def story_height(d, headline, width):
    return 13 + len(wrap(d, headline, F_BOLD(12), width)) * 15 + 7


def draw_story(d, x, y, region, headline, width):
    d.text((x, y), region, font=F_BOLD(10), fill=RED)
    y += 13
    for ln in wrap(d, headline, F_BOLD(12), width):
        d.text((x, y), ln, font=F_BOLD(12), fill=INK)
        y += 15
    return y + 7


def draw_chart(d, x, y, w, h):
    """Market rout: plunging line chart."""
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=PANEL_LINE, width=1)
    d.text((x + 8, y + 6), "MARKETS: THE AI ROUT", font=F_BOLD(10), fill=RED)
    pts = [(x + 14, y + 34), (x + 60, y + 40), (x + 105, y + 30),
           (x + 150, y + 52), (x + 195, y + 66), (x + 240, y + 62),
           (x + 285, y + 92)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.text((x + 8, y + h - 22), "S&P 500  -3.7%   NASDAQ  -5.3%",
           font=F_BOLD(11), fill=INK)


def draw_seismo(d, x, y, w, h):
    """Peru quake seismograph."""
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=PANEL_LINE, width=1)
    d.text((x + 8, y + 6), "PERU: M6.7 QUAKE", font=F_BOLD(10), fill=RED)
    mid = y + h // 2 + 2
    pts = [(x + 10, mid)]
    for i in range(1, 40):
        px = x + 10 + i * (w - 20) / 40
        amp = 18 * math.sin(i * 0.9) * math.exp(-abs(i - 20) / 14.0)
        pts.append((px, mid + amp))
    d.line(pts, fill=INK, width=2)
    d.text((x + 8, y + h - 20), "JUNIN 19:09  ·  FELT IN LIMA",
           font=F_BOLD(11), fill=INK)


def draw_cop(d, x, y, w, h):
    """COP31 Antalya: sun, flags, overtime."""
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=PANEL_LINE, width=1)
    d.text((x + 8, y + 6), "COP31 ANTALYA", font=F_BOLD(10), fill=RED)
    cx, cy = x + w - 46, y + 40
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(232, 164, 32))
    for k in range(8):
        a = k * math.pi / 4
        d.line([(cx + 20 * math.cos(a), cy + 20 * math.sin(a)),
                (cx + 27 * math.cos(a), cy + 27 * math.sin(a))],
               fill=(232, 164, 32), width=2)
    for i, col in enumerate([(178, 34, 34), (30, 64, 120), (34, 120, 60)]):
        fx = x + 14 + i * 34
        d.line([(fx, y + 24), (fx, y + 52)], fill=INK, width=2)
        d.polygon([(fx, y + 24), (fx + 24, y + 30), (fx, y + 38)], fill=col)
    d.text((x + 8, y + h - 38), "Fossil-fuel talks deadlocked.",
           font=F_SANS(12), fill=INK)
    d.text((x + 8, y + h - 20), "Summit into OVERTIME.",
           font=F_BOLD(12), fill=INK)


def draw_columns(d, y_top, y_bottom):
    """Four columns, greedy shortest-column fill. Returns stories drawn."""
    col_w = (W - 2 * MARGIN - 3 * GAP) // 4
    xs = [MARGIN + i * (col_w + GAP) for i in range(4)]
    heights = [story_height(d, h, col_w) for _, h in STORIES]
    cols = [[], [], [], []]
    col_h = [0, 0, 0, 0]
    for idx, hh in enumerate(heights):
        c = col_h.index(min(col_h))
        cols[c].append(idx)
        col_h[c] += hh
    drawn = 0
    for c in range(4):
        y = y_top
        for idx in cols[c]:
            if y + heights[idx] > y_bottom:
                continue
            y = draw_story(d, xs[c], y, STORIES[idx][0], STORIES[idx][1],
                           col_w)
            drawn += 1
            d.line([(xs[c], y - 3), (xs[c] + col_w, y - 3)],
                   fill=(210, 204, 190), width=1)
    return drawn


def draw_panels(d, y, h):
    col_w = (W - 2 * MARGIN - 2 * GAP) // 3
    xs = [MARGIN, MARGIN + col_w + GAP, MARGIN + 2 * (col_w + GAP)]
    draw_chart(d, xs[0], y, col_w, h)
    draw_seismo(d, xs[1], y, col_w, h)
    draw_cop(d, xs[2], y, col_w, h)
    return y + h


def draw_numbers(d, y):
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=3)
    y += 9
    d.text((W // 2, y), "DAY IN NUMBERS", font=F_BOLD(15), fill=RED,
           anchor="ma")
    y += 22
    cell = (W - 2 * MARGIN) // len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        cx = MARGIN + cell * i + cell // 2
        d.text((cx, y), num, font=F_BOLD(22), fill=INK, anchor="ma")
        d.text((cx, y + 26), label, font=F_SANS(11), fill=GREY, anchor="ma")
    return y + 44


def draw_footer(d, y):
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 6
    d.text((W // 2, y),
           "All stories happened or were first reported on Friday 20 November 2026.",
           font=F_SANS(12), fill=GREY, anchor="ma")
    y += 15
    d.text((W // 2, y),
           "Sources: AP · Reuters · WSJ · UN News · USGS · IAEA  —  THE WORLD TODAY",
           font=F_SANS(11), fill=GREY, anchor="ma")
    return y + 13


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 16
    y = draw_masthead(d, y)
    y = draw_lead(d, y)
    drawn = draw_columns(d, y + 2, 790)
    y = draw_panels(d, 798, 96)
    y = draw_numbers(d, y + 8)
    draw_footer(d, y + 4)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path, "| stories drawn:", drawn, "of", len(STORIES))


if __name__ == "__main__":
    main()
