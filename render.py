#!/usr/bin/env python3
"""news-image-20261120 V3 — front page, drawn with Pillow from the V3 brief.

One 1024x1024 newspaper front page summing up Friday 20 November 2026.
Fresh angle (NOT V1/V2's dead recipe): markets is lead #3, bold banner
labels on EVERY story, evidence badges on every tile, 6 newly-verified
20-Nov stories added. NO SO WHAT lines, NO timeline strip, spacious.
35 stories. Run: python3 render.py -> entry.png next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 20
CW = W - 2 * M

# Palette (same cream-paper front page as V1/V2 — the skeleton is proven).
PAPER = (244, 235, 221)
PAPER_L = (250, 246, 235)
INK = (25, 24, 22)
RED = (198, 40, 40)
RED_D = (160, 28, 28)
NAVY = (28, 43, 69)
NAVY_L = (58, 80, 118)
GOLD = (184, 135, 47)
GOLD_L = (214, 172, 90)
WHITE = (255, 253, 246)
LAND = (232, 222, 206)
MAPLINE = (207, 195, 177)
GREY = (105, 96, 88)
NIGHT = (24, 38, 64)
SEA_PALE = (214, 226, 232)
SEA_BLUE = (72, 110, 160)
GREEN = (34, 120, 70)

FDIR = "/usr/share/fonts/truetype/liberation/"

def _f(name, size):
    return ImageFont.truetype(FDIR + name, size)

def serif_b(s): return _f("LiberationSerif-Bold.ttf", s)
def serif_i(s): return _f("LiberationSerif-Italic.ttf", s)
def sans(s): return _f("LiberationSans-Regular.ttf", s)
def sans_b(s): return _f("LiberationSans-Bold.ttf", s)
def sans_i(s): return _f("LiberationSans-Italic.ttf", s)

canvas = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(canvas)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)

def tw(text, font):
    return d.textlength(text, font=font)

def wrap(text, font, max_w):
    out, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if tw(trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out

def block(x, y, text, font, max_w, color, lh=None):
    if lh is None:
        lh = int(font.size * 1.25)
    for ln in wrap(text, font, max_w):
        d.text((x, y), ln, font=font, fill=color)
        y += lh
    return y

def rule(y, x0, x1, color, w=2):
    d.line([(x0, y), (x1, y)], fill=color, width=w)

def pill(box, fill, rad=10):
    d.rounded_rectangle(box, radius=rad, fill=fill)

def banner(x, y, text, fill, font=None):
    """Bold coloured banner label: punchy 2-4 word label, white text."""
    if font is None:
        font = sans_b(11)
    wdt = tw(text, font) + 16
    d.rounded_rectangle([x, y, x + wdt, y + 20], radius=3, fill=fill)
    d.text((x + 8, y + 4), text, font=font, fill=WHITE)
    return wdt

# ---------------------------------------------------------------- eyebrow + masthead
d.text((M, 8), "THE WORLD IN ONE DAY", font=sans_b(11), fill=RED)
top_right = "35 STORIES  \u00b7  7 REGIONS  \u00b7  ONE PAGE"
d.text((W - M - tw(top_right, sans_b(11)), 8), top_right, font=sans_b(11), fill=INK)
rule(24, M, W - M, INK, 2)

d.text((M, 28), "Friday 20 November 2026", font=serif_b(54), fill=INK)
rule(88, M, W - M, RED, 3)

d.text((M, 94), "Kyiv bridges hit  \u00b7  Akvan landfall  \u00b7  AI sell-off  "
                 "\u00b7  Polish missile strike",
       font=serif_i(14), fill=RED)

# ---------------------------------------------------------------- number strip
NUMS = [
    ("~30", "missiles fired at Kyiv"),
    ("300,000+", "evacuated in Odisha"),
    ("\u22126.22%", "Taiwan Taiex, Friday"),
    ("\u221214%", "Nvidia, Friday"),
    ("1,070bp", "Argentina country risk"),
    ("60.7%", "pancreatic cancer response"),
]
ns_y, ns_h = 112, 46
cell = CW / 6
for i, (num, lab) in enumerate(NUMS):
    x0 = M + i * cell
    d.rectangle([x0, ns_y, x0 + cell - 1, ns_y + ns_h], outline=NAVY, width=1)
    d.text((x0 + 8, ns_y + 3), num, font=sans_b(21), fill=RED)
    d.text((x0 + 8, ns_y + 28), lab, font=sans(9), fill=INK)
    d.line([(x0 + 8, ns_y + ns_h - 6), (x0 + 30, ns_y + ns_h - 6)], fill=GOLD, width=2)

# ---------------------------------------------------------------- region strip (no timeline strip in V3)
REGIONS = [("EUROPE", "11", NAVY), ("ASIA", "8", RED), ("AMERICAS", "6", NAVY),
           ("OCEANIA", "4", NAVY), ("MIDDLE EAST", "3", NAVY), ("AFRICA", "2", NAVY),
           ("GLOBAL", "1", GOLD)]
ry = 166
x = M
for name, n, col in REGIONS:
    label = f"{name} {n}"
    wdt = tw(label, sans_b(10)) + 16
    pill([x, ry, x + wdt, ry + 20], col, rad=10)
    d.text((x + 8, ry + 4), label, font=sans_b(10), fill=WHITE)
    x += wdt + 6
rlabel = "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE"
d.text((W - M - tw(rlabel, sans_b(9)), ry + 5), rlabel, font=sans_b(9), fill=INK)

# ================================================================ LEAD ART

def ember(cx, cy, r):
    for rr, a in [(r, 90), (int(r * 0.62), 150), (int(r * 0.34), 230)]:
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 140, 40, a))
    gd.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 220, 120, 255))

def art_kyiv(x0, y0, w, h):
    """Night over the Dnipro: navy sky, stars, moon, skyline with gold
    windows, gold domes, tower and spire, red missile-trail arcs, river,
    three fire glows, bridge deck + arch + cables, red alert band."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NIGHT)
    for sx, sy in [(24, 10), (70, 18), (120, 8), (180, 14), (230, 10), (280, 16),
                   (50, 30), (150, 26), (210, 30), (260, 26)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 1, y0 + sy + 1], fill=(220, 220, 200))
    d.ellipse([x0 + w - 52, y0 + 8, x0 + w - 30, y0 + 30], fill=(240, 230, 200))
    for (ax, ay, bx, by, cx, cy) in [(10, 78, 120, 26, 210, 58),
                                     (60, 88, 170, 34, 260, 66),
                                     (140, 92, 230, 44, 300, 76)]:
        pts = []
        for t in range(21):
            tt = t / 20
            px = (1 - tt) ** 2 * ax + 2 * (1 - tt) * tt * bx + tt ** 2 * cx
            py = (1 - tt) ** 2 * ay + 2 * (1 - tt) * tt * by + tt ** 2 * cy
            pts.append((x0 + px, y0 + py))
        d.line(pts, fill=RED, width=2)
        d.ellipse([x0 + cx - 3, y0 + cy - 3, x0 + cx + 3, y0 + cy + 3], fill=GOLD_L)
    skyline = [(0, 58, 26, 34), (30, 46, 22, 46), (56, 62, 30, 30), (90, 40, 18, 52),
               (112, 54, 26, 38), (142, 48, 20, 44), (166, 60, 30, 32), (200, 44, 16, 48),
               (220, 56, 26, 36), (250, 50, 22, 42), (276, 62, 30, 30)]
    for bx, by, bw, bh in skyline:
        d.rectangle([x0 + bx, y0 + h - 40 - bh + 22, x0 + bx + bw, y0 + h - 18], fill=(10, 16, 30))
        for wx in range(bx + 4, bx + bw - 3, 7):
            for wy in range(y0 + h - 40 - bh + 26, y0 + h - 22, 8):
                if (wx + wy) % 3 == 0:
                    d.rectangle([x0 + wx, wy, x0 + wx + 2, wy + 2], fill=GOLD_L)
    d.rectangle([x0 + 96, y0 + 18, x0 + 104, y0 + h - 18], fill=(10, 16, 30))
    d.polygon([(x0 + 94, y0 + 18), (x0 + 106, y0 + 18), (x0 + 100, y0 + 6)], fill=(10, 16, 30))
    for cx in (x0 + 150, x0 + 236):
        d.pieslice([cx - 9, y0 + h - 58, cx + 9, y0 + h - 40], 180, 360, fill=GOLD)
    d.rectangle([x0, y0 + h - 18, x0 + w, y0 + h], fill=(38, 68, 110))
    for rx in range(0, w, 34):
        d.line([(x0 + rx, y0 + h - 9), (x0 + rx + 18, y0 + h - 9)], fill=(120, 150, 200), width=1)
    ember(x0 + 44, y0 + h - 42, 11)
    ember(x0 + 158, y0 + h - 48, 9)
    ember(x0 + 208, y0 + h - 40, 10)
    by = y0 + h - 22
    d.rectangle([x0, by, x0 + w, by + 6], fill=(8, 12, 24))
    d.arc([x0 + 30, by - 32, x0 + w - 30, by + 24], 180, 360, fill=(8, 12, 24), width=5)
    acx, acy, arx, ary = x0 + w / 2, by - 4, (w - 60) / 2, 28
    for cx in range(x0 + 46, x0 + w - 40, 26):
        t = (cx - acx) / arx
        top = acy - ary * math.sqrt(max(0.0, 1 - t * t))
        d.line([(cx, by), (cx, int(top))], fill=(8, 12, 24), width=2)
    for px in range(x0 + 8, x0 + w, 22):
        d.rectangle([px, by - 3, px + 3, by], fill=GOLD)
    d.rectangle([x0, y0, x0 + w, y0 + 15], fill=RED)
    d.text((x0 + 8, y0 + 3), "AIR ALERT  \u00b7  KYIV  \u00b7  01:25 LOCAL", font=sans_b(9), fill=WHITE)

def art_akvan(x0, y0, w, h):
    """Bay of Bengal: pale sea, cream India landmass right, navy coastline,
    compact cyclone spiral offshore, wind-barb ticks, gold Gopalpur marker,
    rain streaks inland, navy top band."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA_PALE)
    d.polygon([(x0 + 190, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0 + 210, y0 + h),
               (x0 + 196, y0 + 84), (x0 + 208, y0 + 52), (x0 + 196, y0 + 24)],
              fill=(238, 228, 208))
    d.line([(x0 + 190, y0), (x0 + 196, y0 + 24), (x0 + 208, y0 + 52),
            (x0 + 196, y0 + 84), (x0 + 210, y0 + h)], fill=NAVY, width=2)
    d.text((x0 + 228, y0 + 30), "INDIA", font=sans_b(9), fill=NAVY)
    d.text((x0 + 228, y0 + 42), "Odisha", font=sans(8), fill=INK)
    d.text((x0 + 10, y0 + h - 16), "BAY OF BENGAL", font=sans_b(8), fill=NAVY_L)
    cx, cy = x0 + 104, y0 + 62
    for rr, col, wd in [(56, RED, 4), (44, NAVY, 5), (32, PAPER_L, 5),
                        (22, NAVY, 4), (12, RED, 3)]:
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 140, 20, fill=col, width=wd)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=PAPER_L, outline=NAVY, width=2)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        x1 = cx + int(64 * math.cos(a)); y1 = cy + int(64 * math.sin(a))
        x2 = cx + int(74 * math.cos(a)); y2 = cy + int(74 * math.sin(a))
        d.line([(x1, y1), (x2, y2)], fill=NAVY, width=2)
    gx, gy = x0 + 198, y0 + 66
    d.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=GOLD, outline=RED, width=2)
    d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=RED)
    d.rectangle([x0 + 210, y0 + 58, x0 + 288, y0 + 74], fill=NAVY)
    d.text((x0 + 214, y0 + 61), "GOPALPUR", font=sans_b(9), fill=WHITE)
    for sx in range(x0 + 232, x0 + w - 6, 18):
        d.line([(sx, y0 + 84), (sx - 4, y0 + 94)], fill=NAVY_L, width=1)
    d.rectangle([x0, y0, x0 + w, y0 + 15], fill=NAVY)
    d.text((x0 + 8, y0 + 3), "LANDFALL 02:00 UTC  \u00b7  GUSTS 110 KM/H", font=sans_b(9), fill=WHITE)

def art_markets(x0, y0, w, h):
    """Trading floor in free fall: dark red-black board, three plunging
    index lines (Taiex, KOSPI, Nikkei) in red/gold, candlesticks dropping,
    a big -6.22% readout, red top band."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(32, 12, 14))
    for gx in range(x0 + 16, x0 + w, 24):
        d.line([(gx, y0 + 18), (gx, y0 + h - 4)], fill=(70, 40, 42), width=1)
    for gy in range(y0 + 26, y0 + h - 4, 16):
        d.line([(x0 + 4, gy), (x0 + w - 4, gy)], fill=(70, 40, 42), width=1)
    d.line([(x0 + 10, y0 + 26), (x0 + 90, y0 + 30), (x0 + 170, y0 + 44),
            (x0 + 250, y0 + 66), (x0 + w - 10, y0 + 88)], fill=RED, width=3)
    d.line([(x0 + 10, y0 + 32), (x0 + 90, y0 + 38), (x0 + 170, y0 + 54),
            (x0 + 250, y0 + 72), (x0 + w - 10, y0 + 96)], fill=GOLD_L, width=2)
    d.line([(x0 + 10, y0 + 38), (x0 + 90, y0 + 46), (x0 + 170, y0 + 62),
            (x0 + 250, y0 + 80), (x0 + w - 10, y0 + 100)], fill=(220, 120, 120), width=2)
    for i, (cx, top, bot) in enumerate([(40, 30, 44), (80, 36, 52), (120, 44, 62),
                                        (160, 56, 74), (200, 68, 88), (240, 80, 100)]):
        d.rectangle([x0 + cx - 6, y0 + top, x0 + cx + 6, y0 + bot], fill=RED)
        d.line([(x0 + cx, y0 + top - 6), (x0 + cx, y0 + bot + 6)], fill=RED, width=2)
    d.text((x0 + 10, y0 + h - 34), "TAIEX -6.22%", font=sans_b(13), fill=WHITE)
    d.text((x0 + 10, y0 + h - 18), "KOSPI -5.4%  \u00b7  NIKKEI -4.9%  \u00b7  NVDA -14%",
           font=sans_b(9), fill=GOLD_L)
    d.rectangle([x0, y0, x0 + w, y0 + 15], fill=RED)
    d.text((x0 + 8, y0 + 3), "FRIDAY CLOSE  \u00b7  WORST WEEK SINCE 1991", font=sans_b(9), fill=WHITE)


# ---------------------------------------------------------------- lead cards
# V3: banner label on every lead (samatch-we system), data bar, headline,
# body — NO SO WHAT lines.
LEADS = [
    dict(num="01", tag="KYIV", art=art_kyiv, banner="KYIV \u2014 3 BRIDGES HIT", bfill=RED,
         bar="01:25 LOCAL  \u00b7  7 WAVES  \u00b7  ~30 MISSILES",
         head="Russia rains 30 missiles on Kyiv",
         body=("Seven overnight waves from 01:25. Three killed, all water "
               "workers. Energy and transport sites struck; fires in three "
               "districts. Power and water cut."),
         src="Kyiv Post \u00b7 Reuters \u00b7 Kyiv Independent"),
    dict(num="02", tag="ODISHA / AKVAN", art=art_akvan, banner="CYCLONE AKVAN", bfill=NAVY,
         bar="LANDFALL 02:00 UTC  \u00b7  300,000+ EVACUATED",
         head="Akvan hits Gopalpur; 300,000 evacuated",
         body=("Landfall ~08:00 local (02:00 UTC). Winds 70\u2013100 km/h, "
               "gusting 110. 423 rescue teams deployed; schools shut, trains "
               "cancelled. No deaths by midday."),
         src="IMD \u00b7 PTI \u00b7 The Hindu"),
    dict(num="03", tag="MARKETS / ASIA", art=art_markets, banner="AI SELL-OFF", bfill=RED,
         bar="TAIEX \u22126.22%  \u00b7  KOSPI \u22125.4%  \u00b7  NIKKEI \u22124.9%",
         head="AI sell-off sinks Asia; Taiex \u22126.22%",
         body=("Taiwan closes 36,033.29, worst week since 1991 (\u221217%). "
               "TSMC below NT$2,000. KOSPI \u22125.4%, Nikkei \u22124.9%. "
               "Regulator adds short-selling curbs."),
         src="AP \u00b7 Bloomberg"),
]
LY, LH, LW, LG = 194, 268, 320, 12
for i, L in enumerate(LEADS):
    x0 = M + i * (LW + LG)
    d.rectangle([x0, LY, x0 + LW, LY + LH], outline=NAVY, width=1)
    L["art"](x0 + 1, LY + 1, LW - 2, 110)
    d.rectangle([x0, LY + 111, x0 + LW, LY + 126], fill=NAVY)
    d.text((x0 + 8, LY + 115), L["bar"], font=sans_b(8), fill=GOLD_L)
    # Banner label (bold coloured banner, samatch-we system)
    banner(x0 + 8, LY + 131, L["banner"], L["bfill"])
    d.text((x0 + 8, LY + 156), L["num"], font=sans_b(11), fill=RED)
    d.text((x0 + 34, LY + 156), L["tag"], font=sans_b(11), fill=NAVY)
    hy = LY + 172
    hl = wrap(L["head"], serif_b(16), LW - 16)[:2]
    for ln in hl:
        d.text((x0 + 8, hy), ln, font=serif_b(16), fill=INK)
        hy += 18
    by = hy + 4
    bl = wrap(L["body"], sans(10), LW - 16)
    for ln in bl:
        d.text((x0 + 8, by), ln, font=sans(10), fill=INK)
        by += 11
    d.text((x0 + 8, LY + LH - 13), L["src"], font=sans_i(8), fill=GREY)
    print(f"lead {L['num']}: head {len(hl)} lines, body {len(bl)} lines, "
          f"text bottom {by} vs card bottom {LY + LH - 13}")

# ---------------------------------------------------------------- feature tiles
# Thumbnails: cream grounds, navy linework, restrained red/gold accents.

def thumb_chart(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER_L)
    for gx in range(x0 + 20, x0 + w, 22):
        d.line([(gx, y0 + 3), (gx, y0 + h - 3)], fill=(225, 214, 190), width=1)
    pts = [(x0 + 8, y0 + 6), (x0 + 50, y0 + 9), (x0 + 95, y0 + 13),
           (x0 + 140, y0 + 20), (x0 + w - 8, y0 + 27)]
    d.line(pts, fill=RED, width=3)
    d.ellipse([x0 + w - 12, y0 + 23, x0 + w - 4, y0 + 31], fill=RED)
    d.text((x0 + 8, y0 + h - 11), "TAIEX  KOSPI  NIKKEI", font=sans_b(7), fill=NAVY)

def thumb_bars(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER_L)
    for i, v in enumerate([1.6, 1.9, 2.1, 2.2]):
        bx = x0 + 22 + i * 34
        bh = int(v / 2.5 * (h - 12))
        d.rectangle([bx, y0 + h - 5 - bh, bx + 20, y0 + h - 5],
                    fill=RED if i == 3 else NAVY)
    d.text((x0 + 8, y0 + 2), "2.2%", font=sans_b(9), fill=RED)

def thumb_flat(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER_L)
    my = y0 + h // 2
    d.line([(x0 + 8, my), (x0 + w - 8, my)], fill=NAVY, width=3)
    for dx in range(x0 + 20, x0 + w - 10, 26):
        d.ellipse([dx - 2, my - 2, dx + 2, my + 2], fill=GOLD)
    d.text((x0 + 8, y0 + 3), "1-YR 3.0%", font=sans_b(8), fill=NAVY)
    d.text((x0 + w - 62, y0 + h - 12), "5-YR 3.5%", font=sans_b(8), fill=RED)

def thumb_flags(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER_L)
    d.rectangle([x0 + 14, y0 + 5, x0 + 82, y0 + h - 5], fill=(30, 60, 150))
    for k in range(8):
        a = k * math.pi / 4
        sx = x0 + 48 + int(11 * math.cos(a))
        sy = y0 + h // 2 + int(7 * math.sin(a))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=GOLD)
    d.rectangle([x0 + 100, y0 + 5, x0 + w - 14, y0 + h - 5], fill=(30, 60, 150))
    d.line([(x0 + 100, y0 + h // 2), (x0 + w - 14, y0 + h // 2)], fill=WHITE, width=5)
    d.line([(x0 + (100 + w - 14) // 2, y0 + 5), (x0 + (100 + w - 14) // 2, y0 + h - 5)],
           fill=WHITE, width=5)
    d.line([(x0 + 100, y0 + h // 2), (x0 + w - 14, y0 + h // 2)], fill=RED, width=2)
    d.line([(x0 + (100 + w - 14) // 2, y0 + 5), (x0 + (100 + w - 14) // 2, y0 + h - 5)],
           fill=RED, width=2)

def thumb_ballot(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER_L)
    d.rectangle([x0 + 22, y0 + 12, x0 + 82, y0 + h - 5], fill=NAVY)
    d.rectangle([x0 + 34, y0 + 8, x0 + 70, y0 + 12], fill=NAVY)
    d.line([(x0 + 40, y0 + 9), (x0 + 64, y0 + 9)], fill=GOLD, width=2)
    d.rectangle([x0 + 44, y0 - 2, x0 + 60, y0 + 8], fill=WHITE, outline=INK, width=1)
    d.text((x0 + 100, y0 + 8), "2027", font=sans_b(16), fill=GOLD)
    d.text((x0 + 100, y0 + 24), "VOTE", font=sans_b(8), fill=NAVY)

def thumb_globe(x0, y0, w, h):
    """COP31: navy globe with cream continents + red thermometer."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER_L)
    cx, cy, gr = x0 + 60, y0 + h // 2, 13
    d.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=SEA_BLUE, outline=NAVY, width=1)
    d.ellipse([cx - 7, cy - 9, cx + 2, cy - 2], fill=(238, 228, 208))
    d.ellipse([cx - 2, cy + 1, cx + 8, cy + 8], fill=(238, 228, 208))
    tx = x0 + 110
    d.rounded_rectangle([tx, y0 + 4, tx + 12, y0 + h - 4], radius=5, fill=WHITE, outline=NAVY, width=1)
    d.rectangle([tx + 4, y0 + 10, tx + 8, y0 + h - 8], fill=RED)
    d.ellipse([tx - 1, y0 + h - 12, tx + 13, y0 + h - 2], fill=RED, outline=NAVY, width=1)
    d.text((x0 + 140, y0 + 4), "+1.5\u00b0C", font=sans_b(9), fill=RED)
    d.text((x0 + 140, y0 + 16), "GOAL", font=sans_b(7), fill=NAVY)

def thumb_missile(x0, y0, w, h):
    """Poland: Kh-101 cruise missile streaking over farmland, red flash."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    for sx, sy in [(20, 6), (60, 10), (110, 5), (150, 9), (90, 14)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 1, y0 + sy + 1], fill=WHITE)
    d.polygon([(x0 + 40, y0 + 14), (x0 + 130, y0 + 14), (x0 + 148, y0 + 18),
               (x0 + 130, y0 + 22), (x0 + 40, y0 + 22)], fill=(220, 220, 210))
    d.polygon([(x0 + 148, y0 + 18), (x0 + 162, y0 + 14), (x0 + 162, y0 + 22)], fill=RED)
    d.polygon([(x0 + 40, y0 + 14), (x0 + 28, y0 + 10), (x0 + 40, y0 + 18)], fill=GOLD)
    d.ellipse([x0 + 168, y0 + 14, x0 + 176, y0 + 22], fill=GOLD_L)
    d.rectangle([x0, y0 + h - 8, x0 + w, y0 + h], fill=(38, 68, 110))
    d.text((x0 + 8, y0 + h - 7), "KH-101", font=sans_b(7), fill=WHITE)

def thumb_chip(x0, y0, w, h):
    """Nvidia: green chip square on dark board, red -14% slash."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(20, 30, 22))
    d.rectangle([x0 + 60, y0 + 4, x0 + 120, y0 + h - 4], fill=(30, 90, 50), outline=GOLD, width=1)
    d.text((x0 + 72, y0 + 8), "NVDA", font=sans_b(10), fill=WHITE)
    d.line([(x0 + 10, y0 + 8), (x0 + 50, y0 + 12), (x0 + 90, y0 + 20),
            (x0 + 130, y0 + 26), (x0 + w - 10, y0 + 28)], fill=RED, width=2)
    d.text((x0 + 132, y0 + h - 12), "-14%", font=sans_b(11), fill=RED)

def thumb_rig(x0, y0, w, h):
    """Kenya oil: derrick silhouette + sun, gold on cream."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER_L)
    d.ellipse([x0 + w - 30, y0 + 4, x0 + w - 12, y0 + 22], fill=GOLD)
    d.polygon([(x0 + 70, y0 + 28), (x0 + 90, y0 + 28), (x0 + 100, y0 + 4),
               (x0 + 80, y0 + 4)], fill=NAVY)
    d.line([(x0 + 74, y0 + 28), (x0 + 82, y0 + 10)], fill=NAVY, width=2)
    d.line([(x0 + 86, y0 + 28), (x0 + 94, y0 + 10)], fill=NAVY, width=2)
    d.rectangle([x0 + 60, y0 + 26, x0 + 110, y0 + h - 4], fill=(60, 50, 40))
    d.text((x0 + 8, y0 + 4), "AMOSING 1", font=sans_b(8), fill=NAVY)
    d.text((x0 + 130, y0 + h - 12), "20,000 b/d", font=sans_b(8), fill=RED)

def thumb_convoy(x0, y0, w, h):
    """Iraq: convoy of flagged vehicles on a desert road."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 228, 208))
    d.rectangle([x0, y0 + h - 10, x0 + w, y0 + h], fill=(120, 100, 80))
    for i, cx in enumerate([40, 90, 140]):
        d.rectangle([x0 + cx - 14, y0 + 10, x0 + cx + 14, y0 + 20], fill=NAVY)
        d.ellipse([x0 + cx - 8, y0 + 20, x0 + cx - 2, y0 + 26], fill=INK)
        d.ellipse([x0 + cx + 2, y0 + 20, x0 + cx + 8, y0 + 26], fill=INK)
        d.rectangle([x0 + cx - 2, y0 + 2, x0 + cx + 2, y0 + 10], fill=INK)
        d.polygon([(x0 + cx + 2, y0 + 2), (x0 + cx + 12, y0 + 5), (x0 + cx + 2, y0 + 8)],
                  fill=RED if i == 0 else WHITE)
    d.text((x0 + 8, y0 + 2), "JURF AL-SAKHAR", font=sans_b(7), fill=NAVY)

def thumb_arg(x0, y0, w, h):
    """Argentina: plunging peso chart, 1,070bp readout."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER_L)
    for gx in range(x0 + 20, x0 + w, 22):
        d.line([(gx, y0 + 3), (gx, y0 + h - 3)], fill=(225, 214, 190), width=1)
    pts = [(x0 + 8, y0 + 8), (x0 + 50, y0 + 10), (x0 + 95, y0 + 14),
           (x0 + 140, y0 + 22), (x0 + w - 8, y0 + 28)]
    d.line(pts, fill=RED, width=3)
    d.ellipse([x0 + w - 12, y0 + 24, x0 + w - 4, y0 + 32], fill=RED)
    d.text((x0 + 8, y0 + h - 11), "1,070bp  +139", font=sans_b(7), fill=RED)

def thumb_pill(x0, y0, w, h):
    """Pancreatic pill: capsule + 60.7% readout on white."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=WHITE)
    d.rounded_rectangle([x0 + 30, y0 + 8, x0 + 110, y0 + 22], radius=7, fill=RED)
    d.rounded_rectangle([x0 + 30, y0 + 8, x0 + 70, y0 + 22], radius=7, fill=(240, 240, 240))
    d.ellipse([x0 + 130, y0 + 6, x0 + 160, y0 + 24], fill=GREEN)
    d.text((x0 + 136, y0 + 10), "\u2713", font=sans_b(10), fill=WHITE)
    d.text((x0 + 8, y0 + h - 12), "60.7% RESPONSE", font=sans_b(9), fill=RED)

TILES = [
    dict(num="04", tag="ANTALYA \u2014 CLIMATE", banner="COP31: NO DEAL", bfill=NAVY,
         art=thumb_globe, badge="CONFIRMED",
         head="COP31 draft drops fossil fuels",
         body=("$120bn adaptation finance unresolved. Hosts push \u201c35 by 35\u201d "
               "clean power. Talks may run into weekend."),
         src="UN News \u00b7 Reuters \u00b7 AFP"),
    dict(num="05", tag="POLAND \u2014 EUROPE", banner="POLAND: MISSILE", bfill=RED,
         art=thumb_missile, badge="CONFIRMED",
         head="Russian Kh-101 lands in Poland",
         body=("Down near Nowy Lipowiec, ~50km from the border. A 2nd "
               "missile + jet drone also fell. Tusk: provocation."),
         src="AP \u00b7 Reuters"),
    dict(num="06", tag="NEW YORK \u2014 MARKETS", banner="NVIDIA: -14%", bfill=RED,
         art=thumb_chip, badge="REPORTED",
         head="Nvidia -14% on SEC accounting probe",
         body=("Shares close $125.53 after Reuters reports SEC examining its "
               "accounting. Worst week since 2008, -23%."),
         src="Reuters \u00b7 Bloomberg"),
    dict(num="07", tag="TURKANA \u2014 ENERGY", banner="KENYA: OIL", bfill=NAVY,
         art=thumb_rig, badge="OFFICIAL",
         head="Kenya spuds first commercial oil well",
         body=("Gulf Energy starts Amosing 1 in South Lokichar. First "
               "production 1 Dec 2026; target 20,000 b/d."),
         src="Business Daily \u00b7 Kenyan press"),
    dict(num="08", tag="IRAQ \u2014 MIDDLE EAST", banner="IRAQ: ARMY IN", bfill=NAVY,
         art=thumb_convoy, badge="CONFIRMED",
         head="Iraqi forces enter Kataib Hezbollah bastion",
         body=("Deployed in Jurf al-Sakhar, first time in 12 years. PM "
               "al-Zaidi ordered the move over oil smuggling. No resistance."),
         src="Reuters \u00b7 AFP"),
    dict(num="09", tag="BARCELONA \u2014 SCIENCE", banner="PANCREATIC PILL: 60.7%", bfill=GREEN,
         art=thumb_pill, badge="OFFICIAL",
         head="Pancreatic cancer pill shrinks tumours",
         body=("Daraxonrasib plus chemo: 60.7% response, 8.2% complete, "
               "90.2% disease control. 61 patients."),
         src="EORTC-NCI-AACR \u00b7 Revolution Medicines"),
    dict(num="10", tag="BUENOS AIRES \u2014 MARKETS", banner="ARGENTINA: RISK 1,070", bfill=RED,
         art=thumb_arg, badge="CONFIRMED",
         head="Argentina risk crosses 1,000bp",
         body=("Country risk jumps to 1,070 (+139), first time in 13 months. "
               "Bonds slide; peso rates jump."),
         src="JP Morgan EMBI \u00b7 Infobae"),
    dict(num="11", tag="TOKYO \u2014 ECONOMY", banner="JAPAN: CPI 2.2%", bfill=NAVY,
         art=thumb_bars, badge="CONFIRMED",
         head="Japan core inflation 2.2%",
         body=("October core 2.2%, headline 2.3% \u2014 second month above 2%. "
               "December BoJ hike eyed."),
         src="Reuters \u00b7 Jiji"),
    dict(num="12", tag="BRUSSELS \u2014 EUROPE", banner="EU-UK: RESET SUMMIT", bfill=NAVY,
         art=thumb_flags, badge="OFFICIAL",
         head="First EU-UK reset summit in Brussels",
         body=("Costa and von der Leyen host PM Burnham. Food deal, "
               "carbon-market link, 100,000 youth places on table."),
         src="EU Council \u00b7 Reuters"),
    dict(num="13", tag="SAN SALVADOR \u2014 POLITICS", banner="BUKELE: 3RD BID", bfill=NAVY,
         art=thumb_ballot, badge="CONFIRMED",
         head="Bukele files for third term",
         body=("Papers filed before the Thursday night deadline. Vote 28 Feb "
               "2027. Rights groups object."),
         src="AP \u00b7 Al Jazeera"),
]

TW, TG, TH = 188, 11, 148
TY = 468
for idx, T in enumerate(TILES):
    row, col = divmod(idx, 5)
    x0 = M + col * (TW + TG)
    y0 = TY + row * (TH + 6)
    d.rectangle([x0, y0, x0 + TW, y0 + TH], outline=NAVY, width=1)
    T["art"](x0 + 1, y0 + 1, TW - 2, 32)
    # Banner label (bold coloured banner) + evidence badge
    bw = banner(x0 + 6, y0 + 36, T["banner"], T["bfill"], font=sans_b(9))
    d.rounded_rectangle([x0 + TW - 62, y0 + 36, x0 + TW - 4, y0 + 54],
                        radius=3, fill=NAVY)
    d.text((x0 + TW - 58, y0 + 40), T["badge"], font=sans_b(7), fill=WHITE)
    d.text((x0 + 6, y0 + 58), f"{T['num']}  {T['tag']}", font=sans_b(8), fill=RED)
    hy = y0 + 70
    hl = wrap(T["head"], sans_b(12), TW - 12)[:2]
    for ln in hl:
        d.text((x0 + 6, hy), ln, font=sans_b(12), fill=INK)
        hy += 14
    by = hy + 2
    bl = wrap(T["body"], sans(9), TW - 12)[:3]
    for ln in bl:
        d.text((x0 + 6, by), ln, font=sans(9), fill=INK)
        by += 11
    d.text((x0 + 6, y0 + TH - 10), T["src"], font=sans_i(7), fill=GREY)
    print(f"tile {T['num']}: head {len(hl)} lines, body {len(bl)} lines, "
          f"body bottom {by} vs src line {y0 + TH - 10}")


# ---------------------------------------------------------------- bottom: map + ALSO
BY = 776
MAP_W = 310
d.text((M, BY), "WHERE IT HAPPENED", font=sans_b(11), fill=NAVY)
mx, my, mw, mh = M, BY + 14, MAP_W, 86
d.rectangle([mx, my, mx + mw, my + mh], fill=PAPER_L, outline=MAPLINE, width=1)
# Pale continents
d.polygon([(mx + 12, my + 18), (mx + 66, my + 10), (mx + 78, my + 26),
           (mx + 52, my + 38), (mx + 20, my + 34)], fill=LAND)          # N America
d.polygon([(mx + 58, my + 46), (mx + 84, my + 44), (mx + 88, my + 62),
           (mx + 72, my + 76), (mx + 60, my + 60)], fill=LAND)          # S America
d.polygon([(mx + 140, my + 12), (mx + 168, my + 10), (mx + 172, my + 26),
           (mx + 150, my + 32), (mx + 140, my + 22)], fill=LAND)        # Europe
d.polygon([(mx + 142, my + 38), (mx + 172, my + 36), (mx + 178, my + 56),
           (mx + 162, my + 70), (mx + 146, my + 54)], fill=LAND)        # Africa
d.polygon([(mx + 176, my + 10), (mx + 262, my + 8), (mx + 272, my + 26),
           (mx + 240, my + 40), (mx + 196, my + 38), (mx + 178, my + 24)],
          fill=LAND)                                                    # Asia
d.polygon([(mx + 252, my + 56), (mx + 282, my + 54), (mx + 286, my + 66),
           (mx + 258, my + 70)], fill=LAND)                            # Australia
PINS = {1: (186, 20), 2: (226, 38), 3: (256, 38), 4: (176, 36), 5: (156, 22),
        6: (70, 26), 7: (168, 56), 8: (206, 30), 9: (150, 28), 10: (72, 62),
        11: (272, 28), 12: (148, 20), 13: (58, 48)}
for n, (px, py) in PINS.items():
    cx, cy = mx + px, my + py
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED, outline=WHITE, width=1)
    lbl = str(n)
    d.text((cx - tw(lbl, sans_b(7)) / 2, cy - 4), lbl, font=sans_b(7), fill=WHITE)
d.text((M, BY + 104), "1\u20133 LEAD  \u00b7  4\u201313 FEATURE \u2014 35 stories, one Friday.",
       font=sans_b(8), fill=NAVY)

# ALSO list: 22 more stories, 3 columns
AX = M + MAP_W + 12
d.text((AX, BY), "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES", font=sans_b(11), fill=NAVY)
ALSO = [
    ("14", "BEIJING", "LPR held for 18th month: 1-year 3.0%, 5-year 3.5%"),
    ("15", "RIYADH", "Defences intercept Houthi missile, drones"),
    ("16", "HORMUZ", "Strait still shut; Brent near $92.50; 46 ships wait"),
    ("17", "SENEGAL", "Migrant boat capsizes; 4 dead, dozens missing"),
    ("18", "ROME", "CGIL 24-hour general strike; ~100 squares"),
    ("19", "WELLINGTON", "Phillips 118 vs India; first NZ batter, all formats"),
    ("20", "NEW CALEDONIA", "M5.6 quake; no tsunami threat"),
    ("21", "LAS VEGAS", "Russell fastest in wet practice, 1:47.272"),
    ("22", "COOK ISLANDS", "Cyclone Xavier nears Nassau atoll (FORECAST)"),
    ("23", "MERCURY", "BepiColombo arrives; orbit insertion Sat"),
    ("24", "SYDNEY", "Man charged with terror offences; no threat"),
    ("25", "SEOUL", "Ruling party moves to impeach top judge"),
    ("26", "BRASILIA", "Lula meets Chief Raoni; land recognised"),
    ("27", "KHARKIV", "Drone hits hospital; at least four hurt"),
    ("28", "KRYVYI RIH", "Drone attack cuts power to hospitals"),
    ("29", "DNIPRO", "Five injured in drone attack"),
    ("30", "TURIN", "ATP Finals groups end; semis Saturday"),
    ("31", "ANTALYA", "France calls fossil-fuel gap \u201cblack mark\u201d"),
    ("32", "SEOUL", "Court upholds Kakao founder acquittal"),
    ("33", "HONG KONG", "Hang Seng ~20% off January peak"),
    ("34", "ODISHA", "209mm rain at Patrapur as Akvan crosses"),
    ("35", "PORT-AU-PRINCE", "Raid killed 34 gang suspects"),
]
COL_W = 214
also_bottom = 0
for ci in range(3):
    cx = AX + ci * (COL_W + 8)
    cy = BY + 16
    for n, place, fact in ALSO[ci * 8:(ci + 1) * 8] if ci < 2 else ALSO[16:]:
        for ln in wrap(f"{n} {place} \u2014 {fact}", sans(8), COL_W):
            d.text((cx, cy), ln, font=sans(8), fill=INK)
            cy += 10
    also_bottom = max(also_bottom, cy)
print("also bottom:", also_bottom)

# ---------------------------------------------------------------- DATE CHECK
DY = 930
d.rectangle([M, DY, W - M, DY + 46], fill=RED)
d.text((M + 8, DY + 3), "DATE CHECK \u2014 19 NOVEMBER, NOT TODAY\u2019S STORY LIST:",
       font=sans_b(9), fill=WHITE)
dc = ("Shenzhen trilateral summit + peace declaration \u00b7 ICJ Myanmar genocide ruling 9-6 \u00b7 "
      "Anthropic IPO debut (opened $111.50, +34% vs $83; closed $97.17, +17%) \u00b7 UK \u00a3260m drone "
      "package for Ukraine \u00b7 US sanctions on Comancheros + \u2019Ndrangheta \u00b7 US Senate rejects Iran "
      "war-powers 51-48 \u00b7 Houthi strike on Riyadh PIF Tower (Thu) \u00b7 Tanker mine incidents in "
      "Hormuz (Thu) \u00b7 Georgia gas explosion, 6 dead (Thu) \u00b7 UK+Norway \u00a3100m+ for two Ukrainian "
      "naval craft \u00b7 Serbia speaker elected \u00b7 Suneung exam \u00b7 COP31 first draft \u00b7 Voyager 1 one "
      "light-day \u00b7 Van Gogh $190.4m \u00b7 Pew Islam projection.")
block(M + 8, DY + 15, dc, sans(8), CW - 16, WHITE, lh=10)

# ---------------------------------------------------------------- sources + note
d.text((M, 984), "SOURCES: Reuters, AP, AFP, Bloomberg, PTI, IMD, Kyiv Post, Kyiv Independent, UN News, "
                  "EU Council, PBOC, ICC, USGS, ESA, Formula1.com, Al Jazeera, SBS, RNZ, Xinhua, ATP.",
       font=sans(8), fill=INK)
d.text((M, 998), "Every story here happened, or was first reported, on Friday 20 November 2026. "
                  "Claims are attributed; forecasts are flagged.",
       font=sans_i(8), fill=GREY)

canvas = Image.alpha_composite(canvas.convert("RGBA"), glow).convert("RGB")
canvas.save(OUT, "PNG")
print("saved", OUT, canvas.size)
