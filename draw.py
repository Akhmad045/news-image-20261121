#!/usr/bin/env python3
"""Fresh broadsheet front page for 21 November 2026. Pillow only, deterministic."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
BASE = "/usr/share/fonts/truetype/dejavu"
PAPER = (250, 244, 230)
INK = (22, 20, 18)
RED = (178, 24, 28)
DARKRED = (150, 18, 22)
GOLD = (176, 132, 38)
GREY = (92, 86, 78)
LIGHT = (238, 230, 214)
HAIR = (120, 110, 96)

def font(name, size):
    return ImageFont.truetype(os.path.join(BASE, name), size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(s, f):
    return d.textlength(s, font=f)

def centred(y, s, f, fill=INK, x0=0, x1=W):
    w = text_w(s, f)
    d.text(((x0 + x1 - w) / 2, y), s, font=f, fill=fill)

def wrap(s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def para(x, y, s, f, max_w, lh, fill=INK):
    for line in wrap(s, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y

def centred_para(cx, y, s, f, max_w, lh, fill=INK):
    for line in wrap(s, f, max_w):
        centred(y, line, f, fill, cx - max_w // 2, cx + max_w // 2)
        y += lh
    return y

def rule(y, x0, x1, wdt, fill=INK):
    d.rectangle([x0, y, x1, y + wdt - 1], fill=fill)

def chip(x, y, s, f, fill=RED, fg=(255, 255, 255)):
    tw = text_w(s, f)
    pad_x, pad_y = 8, 4
    d.rectangle([x, y, x + tw + 2 * pad_x, y + f.size + 2 * pad_y], fill=fill)
    d.text((x + pad_x, y + pad_y), s, font=f, fill=fg)
    return x + tw + 2 * pad_x

def diamond(cx, cy, r, fill=RED):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)

# ---- outer frame: heavy outer rule + hairline inside ----
d.rectangle([10, 10, 1013, 1013], outline=INK, width=4)
d.rectangle([20, 20, 1003, 1003], outline=HAIR, width=1)

# ---- masthead ----
centred(30, "MORNING EDITION  ·  ONE IMAGE, ONE DAY", F_SANS_B(15), fill=INK)
rule(56, 28, 996, 3)
centred(66, "WORLD NEWS", F_SERIF_B(86), fill=INK)
rule(164, 28, 996, 3)

# ---- date band: red rules, large red serif date, red diamonds ----
rule(176, 28, 996, 2, fill=RED)
date_s = "SATURDAY, 21 NOVEMBER 2026"
df = F_SERIF_B(35)
dw = text_w(date_s, df)
cx = 512
d.text((cx - dw / 2, 184), date_s, font=df, fill=DARKRED)
diamond(cx - dw / 2 - 34, 202, 8)
diamond(cx + dw / 2 + 34, 202, 8)
rule(226, 28, 996, 2, fill=RED)

# ---- lead story ----
y = 240
chip(28, y, "LEAD STORY", F_SANS_B(13))
d.text((152, y + 3), "WAR  ·  WARSAW", font=F_SANS_B(16), fill=INK)
# headline: shrink until it fits on one line (<= two lines allowed)
headline = "Russian missile crashes in Poland"
size = 56
while size > 34:
    hf = F_SERIF_B(size)
    if text_w(headline, hf) <= 948:
        break
    size -= 2
centred(268, headline, F_SERIF_B(size))

# lead panel (left) + caption (right)
px, py, pw, ph = 28, 322, 566, 132
d.rectangle([px, py, px + pw, py + ph], fill=(28, 44, 56))
d.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)
# stylised landmass
d.polygon([(px + 30, py + 118), (px + 120, py + 42), (px + 250, py + 28),
           (px + 380, py + 52), (px + 500, py + 34), (px + 545, py + 70),
           (px + 520, py + 118), (px + 380, py + 126), (px + 210, py + 122)],
          fill=(74, 104, 88))
d.polygon([(px + 90, py + 96), (px + 170, py + 62), (px + 260, py + 78),
           (px + 210, py + 112)], fill=(96, 128, 106))
# dotted border line (country edge)
for i in range(0, 9):
    x0 = px + 70 + i * 48
    d.line([(x0, py + 20), (x0 + 26, py + 20)], fill=GOLD, width=2)
# missile trail arcing down to impact
pts = []
for i in range(21):
    t = i / 20.0
    x = px + 90 + t * 330
    yy = py + 18 + t * t * 82
    pts.append((x, yy))
d.line(pts, fill=(240, 235, 220), width=3)
# missile dot at trail head
d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=(255, 255, 255))
# red burst at impact
ix, iy = px + 430, py + 104
for ang, ln in [(0, 18), (45, 14), (90, 18), (135, 14), (180, 18), (225, 14), (270, 18), (315, 14)]:
    import math
    dx, dy = math.cos(math.radians(ang)) * ln, math.sin(math.radians(ang)) * ln
    d.line([(ix, iy), (ix + dx, iy + dy)], fill=RED, width=4)
d.ellipse([ix - 9, iy - 9, ix + 9, iy + 9], fill=RED)
d.ellipse([ix - 4, iy - 4, ix + 4, iy + 4], fill=(255, 210, 60))
# jet silhouettes (small, top right)
for jx, jy in [(px + 470, py + 22), (px + 505, py + 38)]:
    d.polygon([(jx, jy), (jx + 22, jy + 4), (jx, jy + 8), (jx + 5, jy + 4)], fill=(220, 220, 215))
    d.polygon([(jx + 8, jy + 1), (jx + 14, jy - 5), (jx + 16, jy + 1)], fill=(220, 220, 215))
d.text((px + 10, py + 6), "POLAND", font=F_SANS_B(11), fill=(240, 235, 220))
d.text((px + 452, py + 112), "IMPACT", font=F_SANS_B(10), fill=(255, 210, 60))

# caption right of panel
cx0, cw = 612, 384
y2 = py + 2
d.text((cx0, y2), "WARSAW —", font=F_SANS_B(14), fill=INK)
cap = ("A Russian Kh-101 cruise missile came down in south-east Poland during a "
       "huge air attack on Ukraine; no injuries, NATO jets scrambled. Russian "
       "missiles also hit three Kyiv crossings; at least nine dead in the assault.")
y2 = para(cx0, y2 + 20, cap, F_SANS(13), cw, 17)
rule(y2 + 4, cx0, 996, 1, fill=HAIR)
y2 += 10
d.text((cx0, y2), "MISSILE   Kh-101 · NO INJURIES", font=F_SANS_B(12), fill=DARKRED)
y2 += 18
d.text((cx0, y2), "KYIV   Three bridges hit", font=F_SANS_B(12), fill=DARKRED)

# ---- divider ----
dy = 478
rule(dy + 10, 28, 380, 1, fill=HAIR)
centred(dy, "AROUND THE WORLD", F_SANS_B(15))
rule(dy + 10, 644, 996, 1, fill=HAIR)

# ---- scene panels (48px tall) ----
def scene_globe(x, y, w, h=48):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    cx, cy, r = x + w // 2, y + h // 2 + 2, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 130, 190))
    d.ellipse([cx - 12, cy - 14, cx + 2, cy - 2], fill=(96, 168, 96))
    d.ellipse([cx - 2, cy + 4, cx + 14, cy + 16], fill=(96, 168, 96))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=1)
    # small flags at sides
    for fx, col in [(x + 14, (200, 40, 40)), (x + w - 34, (40, 90, 180))]:
        d.line([(fx + 4, y + 8), (fx + 4, y + 40)], fill=INK, width=2)
        d.rectangle([fx + 4, y + 8, fx + 22, y + 20], fill=col)

def scene_chart(x, y, w, h=48):
    d.rectangle([x, y, x + w, y + h], fill=(246, 236, 222))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    d.line([(x + 12, y + 8), (x + 12, y + h - 8)], fill=INK, width=1)
    d.line([(x + 12, y + h - 8), (x + w - 10, y + h - 8)], fill=INK, width=1)
    pts = [(x + 22, y + 10), (x + 70, y + 14), (x + 120, y + 22), (x + 170, y + 20),
           (x + 220, y + 32), (x + 265, y + 40)]
    d.line(pts, fill=RED, width=3)
    for px_, py_ in pts:
        d.ellipse([px_ - 3, py_ - 3, px_ + 3, py_ + 3], fill=RED)
    d.polygon([(x + 258, y + 33), (x + 272, y + 40), (x + 258, y + 43)], fill=RED)

def scene_europe(x, y, w, h=48):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 246))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    # UK flag (simplified cross) left, EU flag right, linked
    ux, ex = x + 52, x + w - 112
    d.rectangle([ux, y + 10, ux + 58, y + 38], fill=(30, 60, 140))
    d.rectangle([ux, y + 22, ux + 58, y + 26], fill=(255, 255, 255))
    d.rectangle([ux + 27, y + 10, ux + 31, y + 38], fill=(255, 255, 255))
    d.rectangle([ex, y + 10, ex + 58, y + 38], fill=(20, 50, 150))
    for k in range(8):
        import math
        a = math.radians(k * 45)
        sx, sy = ex + 29 + 11 * math.cos(a), y + 24 + 9 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 60))
    # link / handshake arc between flags
    d.line([(ux + 58, y + 24), (ex, y + 24)], fill=GOLD, width=3)
    d.ellipse([x + w // 2 - 6, y + 18, x + w // 2 + 6, y + 30], outline=GOLD, width=3)

def scene_tankers(x, y, w, h=48):
    d.rectangle([x, y, x + w, y + h], fill=(196, 222, 236))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    d.rectangle([x, y + 30, x + w, y + h], fill=(52, 96, 140))
    for tx, tw_ in [(x + 18, 110), (x + 150, 130), (x + 300, 100)]:
        d.rectangle([tx, y + 20, tx + tw_, y + 34], fill=(30, 30, 34))
        d.rectangle([tx + tw_ - 26, y + 12, tx + tw_ - 8, y + 20], fill=(30, 30, 34))
        d.rectangle([tx + 8, y + 14, tx + 16, y + 20], fill=(200, 40, 40))
    for wx in (x + 40, x + 210, x + 380):
        d.line([(wx, y + 38), (wx + 36, y + 38)], fill=(255, 255, 255), width=2)

def scene_datacentre(x, y, w, h=48):
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 238))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    bx = x + w // 2 - 140
    d.rectangle([x, y + 40, x + w, y + 42], fill=(120, 126, 134))
    d.rectangle([bx, y + 8, bx + 280, y + 40], fill=(70, 80, 96))
    d.rectangle([bx, y + 8, bx + 280, y + 14], fill=(52, 60, 74))
    for i in range(8):
        wx = bx + 12 + i * 33
        d.rectangle([wx, y + 19, wx + 22, y + 35], fill=(120, 200, 220))
    d.rectangle([bx + 130, y + 2, bx + 150, y + 8], fill=GOLD)
    d.line([(bx + 40, y + 8), (bx + 40, y + 3)], fill=INK, width=2)
    d.ellipse([bx + 37, y + 1, bx + 43, y + 7], fill=RED)

# ---- story cell ----
def story_cell(x, y, w, section, dateline, scene_fn, headline, caption, fact):
    chip(x, y, section, F_SANS_B(11))
    d.text((x + text_w(section, F_SANS_B(11)) + 22, y + 2), dateline, font=F_SANS_B(12), fill=INK)
    y += 24
    scene_fn(x, y, w)
    y += 48 + 7
    y = centred_para(x + w // 2, y, headline, F_SERIF_B(19), w, 23)
    y += 4
    y = para(x, y, caption, F_SANS(12), w, 16)
    y += 3
    if fact:
        fsize = 11
        while fsize > 9 and text_w(fact, F_SANS_B(fsize)) > w:
            fsize -= 1
        y = para(x, y, fact, F_SANS_B(fsize), w, 15, fill=DARKRED)
    return y

grid_top = 512
col_w = 304
gutter = 14
x1, x2, x3 = 28, 28 + col_w + gutter, 28 + 2 * (col_w + gutter)

story_cell(x1, grid_top, col_w, "CLIMATE", "ANTALYA", scene_globe,
           "COP31 runs into overtime with no deal",
           "Summit misses its Friday close; the latest draft drops every mention of "
           "fossil fuels and the $120bn adaptation target. A third text is due Saturday morning.",
           "DRAFT  Fossil fuels deleted · $120BN DROPPED")
story_cell(x2, grid_top, col_w, "MARKETS", "NEW YORK", scene_chart,
           "Wall Street slides into correction",
           "AI-led sell-off deepens: S&P 500 −3.7%, Nasdaq −5.3%, Dow −1.9%. "
           "Nvidia falls 13.8% as the SEC examines accounting issues.",
           "S&P −3.7% · NASDAQ −5.3% · NVIDIA −13.8%")
story_cell(x3, grid_top, col_w, "EUROPE", "BRUSSELS", scene_europe,
           "UK and EU strike landmark post-Brexit deal",
           "Most food and farm trade checks scrapped from March 2028, carbon markets "
           "linked from January 2028, and a youth mobility scheme for up to 100,000 people a side.",
           "CHECKS SCRAPPED MAR 2028 · YOUTH SCHEME 100,000")
rule(734, 28, 996, 1, fill=HAIR)

row2_top = 748
wide_w = 472
story_cell(28, row2_top, wide_w, "ENERGY", "KHARG ISLAND", scene_tankers,
           "Iran tankers mass to test US blockade",
           "More than 14 Iranian-flagged tankers gather at Kharg Island to sail as a "
           "convoy; Trump says there is no hurry and defers any strike decision until after the New Year.",
           "14+ TANKERS · DECISION AFTER NEW YEAR")
story_cell(524, row2_top, wide_w, "TECH", "WASHINGTON", scene_datacentre,
           "Trump threatens tax on AI data centres abroad",
           "US firms building data centres overseas face a 'tremendous tax', Trump says, "
           "citing Google's Finland project. No policy yet.",
           "'TREMENDOUS TAX' · NOT YET POLICY")

# ---- footer ----
rule(928, 28, 996, 3)
centred(940, "Sources: wire reports, 21 November 2026  ·  WORLD NEWS sums up one day in one image",
        F_SANS(11), fill=GREY)
centred(958, "ALSO: New York to close Rikers Island jail by 2032", F_SANS_B(12))
centred(976, "make.fun  ·  ref 4g7knchf", F_SANS(11), fill=GREY)

img.save("entry.png", format="PNG")
print("saved entry.png", img.size)
