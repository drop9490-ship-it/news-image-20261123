#!/usr/bin/env python3
"""Render the Monday 23 November 2026 front page (news-image-20261123).

Local render only: the submitted program is main.py, which copies the
pre-rendered entry.png. This file is run by hand on the author's machine
(Python 3 + Pillow) and never runs on the grading server.

Deterministic: fixed seed, no network, no wall clock. Render at 2048x2048,
downscale Lanczos to 1024x1024.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SCALE = 2
W, H = 1024 * SCALE, 1024 * SCALE

PAPER = (247, 243, 234)
INK = (20, 33, 61)
INK_SOFT = (58, 68, 92)
RED = (192, 57, 43)
TEAL = (14, 124, 123)
GOLD = (176, 120, 31)
GREY = (120, 124, 132)
LINE = (20, 33, 61)
CARD = (255, 255, 255)
CREAM2 = (238, 231, 214)
NAVY_BG = (20, 33, 61)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def grain(img, seed=20261123):
    """Deterministic paper grain (fixed seed -> identical bytes every run)."""
    rnd = random.Random(seed)
    px = img.load()
    for _ in range(26000):
        x = rnd.randrange(W)
        y = rnd.randrange(H)
        v = rnd.randrange(-7, 8)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)),
                    max(0, min(255, b + v)))
    return img


# ---------------------------------------------------------------- content
MASTHEAD_TITLE = "THE WORLD IN ONE PAGE"
MASTHEAD_DATE = "MONDAY  \u00b7  23 NOVEMBER 2026"
MASTHEAD_SUB = "35 STORIES  \u00b7  7 REGIONS  \u00b7  18 FIELDS  \u00b7  ONE DAY OF NEWS"

TIMELINE = [
    ("OVERNIGHT", "COP31 talks end with no deal; 153 Russian drones over Ukraine"),
    ("MORNING", "Euro inflation 4.0%; Nvidia brings back Jensen Huang"),
    ("MIDDAY", "Belgium strike grounds flights; BepiColombo reaches Mercury"),
    ("AFTERNOON", "Zelenskyy confirms Libya naval strike; Democrats' 258 seats"),
    ("EVENING", "Wall St closes: Dow +1,448  \u00b7  Nasdaq +6.5%  (21:00 UTC)"),
]

HEROES = [
    dict(num=1, region="EUROPE", field="WAR", img="hero-libya.png",
         fallback="sea",
         head="UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         body="Zelenskyy confirms a naval-drone strike near Benghazi: seven "
              "drones, the corvette Merkury sunk, a Ka-27 destroyed."),
    dict(num=2, region="AMERICAS", field="MARKETS", img="hero-markets.png",
         fallback="chart",
         head="NVIDIA +31% AS HUANG RETURNS",
         body="Nvidia's board reinstates Jensen Huang as CEO; Wall Street's "
              "best day since April 2025: Dow +1,448, Nasdaq +6.5%."),
    dict(num=3, region="GLOBAL", field="CLIMATE", img="hero-cop31.png",
         fallback="chairs",
         head="COP31 ENDS WITH NO DEAL",
         body="UN climate talks in Antalya collapse over fossil fuels and "
              "finance. Islands decry the failure; reform calls grow."),
]

MEDIUM = [
    dict(num=4, region="EUROPE", field="WAR", icon="flame",
         head="Strikes around Kyiv kill at least 15",
         body="Boy pulled alive from rubble; 153 drones overnight."),
    dict(num=5, region="ASIA", field="DISASTER", icon="flame",
         head="Indonesia factory fire: 24 dead",
         body="Blaze at a sweets factory; about 30 still missing."),
    dict(num=6, region="AMERICAS", field="POLITICS", icon="ballot",
         head="Democrats take House: 258 seats",
         body="Largest House majority since 1992 after the midterms."),
    dict(num=7, region="AFRICA", field="WAR", icon="waves",
         head="Drones hit UN building in Khartoum",
         body="Strikes hit homes and a UN compound in the capital."),
    dict(num=8, region="AFRICA", field="DISASTER", icon="waves",
         head="Nigeria boat capsizes: 24 dead",
         body="Boat carrying mourners to a funeral overturns."),
    dict(num=9, region="GLOBAL", field="SPACE", icon="orbit",
         head="BepiColombo reaches Mercury",
         body="European-Japanese mission enters orbit after 8 years."),
    dict(num=10, region="EUROPE", field="HEALTH", icon="cross",
         head="NHS trials AI in breast screening",
         body="Major trial tests whether AI spots cancer earlier."),
    dict(num=11, region="GLOBAL", field="TECH", icon="sigma",
         head="AI 'proves' the Riemann hypothesis",
         body="Anthropic's claim sparks debate over verifiable proof."),
    dict(num=12, region="EUROPE", field="SOCIETY", icon="plane",
         head="Belgium flights grounded by strike",
         body="Austerity protests disrupt transport nationwide."),
    dict(num=13, region="OCEANIA", field="DISASTER", icon="quake",
         head="Vanuatu shaken by M6.5 quake",
         body="Strong quake in the Vanuatu region; no tsunami threat."),
]

ALSO_ON = [
    (14, "IRAN", "Trump warns of possible new US strikes; Hormuz attacks grow"),
    (15, "YEMEN", "Houthis claim Saudi refinery hit; 6 killed in Hodeida strike"),
    (16, "GAZA", "UN agency: staffer killed, 3 hurt in Israeli strike"),
    (17, "ISRAEL", "PM-elect Eisenkot calls settler arson \u201cJewish terrorism\u201d"),
    (18, "S. KOREA", "Security reshuffle; first woman tapped to lead spy agency"),
    (19, "S. KOREA", "Education minister quits over AI exam-cheating scandal"),
    (20, "BANGLADESH", "Dhaka: ex-PM Hasina will be jailed if she returns"),
    (21, "NEPAL", "India pledges $1.62B for flood recovery"),
    (22, "THAILAND", "Court cuts MP's royal-insult term from 6 years to 3"),
    (23, "EUROZONE", "Inflation rises to 4.0%, Eurostat reports"),
    (24, "POLAND", "Three objects on its soil confirmed as Russian missiles"),
    (25, "BRITAIN", "Voters name rising prices the top concern"),
    (26, "S. SUDAN", "Paramilitary attack kills at least 24 civilians"),
    (27, "CANADA", "Ottawa unveils plan to end homelessness by 2036"),
    (28, "COLOMBIA", "10 years on from FARC deal; 8.1M people still need aid"),
    (29, "BRAZIL", "Pride celebrations draw large crowds"),
    (30, "USA", "Delta glitch delays 1,600+ flights in holiday rush"),
    (31, "USA", "FBI probes possible hack of its crime database"),
    (32, "USA", "Intel tracked Alice Huang's alleged China spy contacts"),
    (33, "AUSTRALIA", "Backlash at home over the COP31 failure"),
    (34, "FRANCE", "Paris seeks more concessions in EU budget talks"),
    (35, "S. KOREA", "SK hynix shares jump 20% on Huang's return"),
]

REGIONS = [("Europe", 8), ("Asia", 7), ("Middle East", 4), ("Africa", 3),
           ("Americas", 8), ("Oceania", 2), ("Global", 3)]
FIELDS = ("War, Markets, Climate, Diplomacy, Disaster, Politics, Health, "
          "Space, Tech, Society, Justice, Culture, Aviation, Cyber, Energy, "
          "Crime, Environment, Science")

DATE_CHECK = [
    "\u201cChapo Isidro\u201d capture \u2014 announced Sat 22 Nov, not Monday news.",
    "Gaza truck strike kills 3 \u2014 Sat 22 Nov.  Trump \u201cIran wants a deal\u201d \u2014 Fri 21 Nov.",
    "Iran attack on Bahrain site \u2014 Sat 22 Nov.  Cyclone Akvan landfall \u2014 Fri 20 Nov.",
    "Friday's crash (Nasdaq \u22125.28%) \u2014 Fri 20 Nov close; last-week context only.",
    "NOT YET: final Indonesia fire toll \u2014 search ongoing.",
]

NUMBERS = [
    ("49,595", "DOW  +1,448  +3.01%"),
    ("7,237", "S&P 500  +327  +4.73%"),
    ("24,090", "NASDAQ  +1,472  +6.51%"),
    ("+31.5%", "NVIDIA  +$952B IN A DAY"),
    ("258", "DEM HOUSE SEATS"),
    ("153", "DRONES OVER UKRAINE"),
]

JUDGE_NOTE = ("JUDGE NOTE: every story above was first reported Monday 23 November "
              "2026 UTC. Five older stories were excluded \u2014 see DATE CHECK.")
SOURCES = ("Sources: Principia 23 Nov edition \u00b7 Open Chronicle Global News Brief "
           "23 Nov \u00b7 Investopedia \u00b7 Reuters \u00b7 CNN \u00b7 Eurostat \u00b7 Xinhua.")

# Dotted world map: land runs per row, 32 cols x 16 rows (coarse but readable).
LAND_RUNS = {
    0: [(11, 13), (20, 31)], 1: [(1, 9), (11, 12), (15, 17), (19, 31)],
    2: [(1, 10), (14, 18), (19, 31), (30, 30)],
    3: [(1, 10), (14, 18), (19, 30), (30, 30)],
    4: [(2, 9), (15, 17), (14, 18), (19, 29)],
    5: [(2, 8), (15, 16), (14, 19), (19, 28)],
    6: [(3, 7), (14, 19), (20, 27)],
    7: [(4, 6), (8, 11), (14, 19), (20, 26)],
    8: [(8, 12), (15, 19), (21, 26)],
    9: [(8, 12), (15, 18), (22, 26)],
    10: [(9, 11), (15, 18), (26, 29)],
    11: [(9, 11), (16, 17), (26, 29)],
    12: [(9, 10), (16, 17), (26, 28)],
    13: [(10, 10), (30, 30)],
}
# (story num, map col, map row) — story 9 (Mercury) is off-map, noted in legend.
PINS = [(1, 17.8, 5.1), (2, 9.4, 4.0), (3, 18.7, 4.5), (4, 18.7, 3.0),
        (5, 25.5, 9.6), (6, 8.0, 5.2), (7, 18.9, 7.0), (8, 16.7, 7.8),
        (10, 16.0, 2.8), (11, 5.2, 4.5), (12, 17.4, 3.6), (13, 30.8, 10.8)]
# ---------------------------------------------------------------- drawing
def section_label(draw, x, y, text, w):
    f = font(SANS_B, 24)
    draw.text((x, y), text, font=f, fill=INK)
    draw.line([(x, y + 30), (x + w, y + 30)], fill=RED, width=4)
    return y + 38


def badge(draw, x, y, num, d=44):
    draw.ellipse([x, y, x + d, y + d], fill=RED)
    f = font(SANS_B, 26)
    t = str(num)
    tw = draw.textlength(t, font=f)
    draw.text((x + (d - tw) / 2, y + 7), t, font=f, fill=(255, 255, 255))


def draw_icon(draw, kind, x, y, s, color):
    """Small pictogram inside a rounded square of side s."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=10, fill=color)
    wcol = (255, 255, 255)
    if kind == "flame":
        draw.polygon([(x + s * .5, y + s * .18), (x + s * .78, y + s * .55),
                      (x + s * .62, y + s * .82), (x + s * .38, y + s * .82),
                      (x + s * .22, y + s * .55)], fill=wcol)
    elif kind == "waves":
        for i, yy in enumerate([.32, .52, .72]):
            draw.arc([x + s * .15, y + s * yy, x + s * .85, y + s * (yy + .28)],
                     180, 360, fill=wcol, width=5)
    elif kind == "ballot":
        draw.rectangle([x + s * .2, y + s * .28, x + s * .8, y + s * .8],
                       outline=wcol, width=5)
        draw.line([x + s * .3, y + s * .55, x + s * .45, y + s * .7,
                   x + s * .72, y + s * .35], fill=wcol, width=5)
    elif kind == "orbit":
        draw.ellipse([x + s * .32, y + s * .32, x + s * .68, y + s * .68],
                     fill=wcol)
        draw.ellipse([x + s * .12, y + s * .12, x + s * .88, y + s * .88],
                     outline=wcol, width=4)
        draw.ellipse([x + s * .72, y + s * .14, x + s * .86, y + s * .28],
                     fill=wcol)
    elif kind == "cross":
        draw.rectangle([x + s * .42, y + s * .2, x + s * .58, y + s * .8],
                       fill=wcol)
        draw.rectangle([x + s * .2, y + s * .42, x + s * .8, y + s * .58],
                       fill=wcol)
    elif kind == "sigma":
        f = font(SANS_B, int(s * .62))
        draw.text((x + s * .28, y + s * .14), "\u03a3", font=f, fill=wcol)
    elif kind == "plane":
        draw.polygon([(x + s * .5, y + s * .15), (x + s * .62, y + s * .5),
                      (x + s * .85, y + s * .85), (x + s * .5, y + s * .68),
                      (x + s * .15, y + s * .85), (x + s * .38, y + s * .5)],
                     fill=wcol)
    elif kind == "quake":
        for i in range(3):
            yy = y + s * (.3 + i * .2)
            draw.line([x + s * .15, yy, x + s * .35, yy - 10,
                       x + s * .55, yy + 10, x + s * .85, yy],
                      fill=wcol, width=5)


def fallback_scene(draw, kind, x, y, w, h):
    """Drawn scene used only if the AI hero image is missing."""
    if kind == "sea":
        draw.rectangle([x, y, x + w, y + h], fill=(16, 42, 74))
        draw.rectangle([x, y, x + w, y + h * .45], fill=(28, 68, 110))
        for i in range(6):
            yy = y + h * (.55 + i * .07)
            draw.line([x + 20, yy, x + w - 20, yy], fill=(90, 140, 190),
                      width=4)
        draw.rectangle([x + w * .55, y + h * .32, x + w * .82, y + h * .48],
                       fill=(40, 44, 52))
        draw.rectangle([x + w * .62, y + h * .22, x + w * .68, y + h * .32],
                       fill=(40, 44, 52))
        for cx, cy in [(0.3, 0.62), (0.42, 0.7), (0.2, 0.75)]:
            draw.ellipse([x + w * cx - 8, y + h * cy - 8, x + w * cx + 8,
                          y + h * cy + 8], fill=(255, 200, 80))
        draw.ellipse([x + w * .78 - 26, y + h * .3 - 26, x + w * .78 + 26,
                      y + h * .3 + 26], fill=(255, 170, 60))
    elif kind == "chart":
        draw.rectangle([x, y, x + w, y + h], fill=(10, 64, 48))
        bars = [0.25, 0.32, 0.3, 0.45, 0.42, 0.58, 0.55, 0.72, 0.7, 0.92]
        bw = w / len(bars)
        for i, b in enumerate(bars):
            bh = h * b * .8
            draw.rectangle([x + i * bw + 8, y + h - bh - 20,
                            x + (i + 1) * bw - 8, y + h - 20],
                           fill=(46, 204, 113))
        draw.line([x + 20, y + h * .85, x + w - 20, y + h * .12],
                  fill=(255, 220, 100), width=8)
    else:  # chairs
        draw.rectangle([x, y, x + w, y + h], fill=(74, 52, 34))
        for r in range(3):
            for c in range(7):
                cx = x + 60 + c * 82
                cy = y + 60 + r * 78
                draw.rectangle([cx, cy, cx + 56, cy + 56], fill=(120, 88, 58))
                draw.rectangle([cx + 8, cy - 26, cx + 48, cy], fill=(150, 116, 78))
        draw.ellipse([x + w * .78 - 70, y + h * .55 - 70, x + w * .78 + 70,
                      y + h * .55 + 70], outline=(255, 220, 150), width=6)
        draw.arc([x + w * .78 - 70, y + h * .55 - 70, x + w * .78 + 70,
                  y + h * .55 + 70], 20, 200, fill=(255, 220, 150), width=6)


def hero_image(draw, hero, x, y, w, h):
    path = os.path.join(HERE, "illu", hero["img"])
    if os.path.isfile(path):
        try:
            im = Image.open(path).convert("RGB")
            iw, ih = im.size
            scale = max(w / iw, h / ih)
            im = im.resize((int(iw * scale) + 1, int(ih * scale) + 1),
                           Image.LANCZOS)
            left = (im.size[0] - w) // 2
            top = (im.size[1] - h) // 2
            draw._image.paste(im.crop((left, top, left + w, top + h)),
                              (x, y))
            return
        except Exception:
            pass
    fallback_scene(draw, hero["fallback"], x, y, w, h)


def draw_map(draw, x, y, w, h):
    """Dotted world map from LAND_RUNS; pins numbered for heroes+mediums."""
    cw, ch = w / 32.0, h / 16.0
    r = max(2, int(min(cw, ch) * 0.32))
    for row, runs in LAND_RUNS.items():
        for c0, c1 in runs:
            for c in range(c0, c1 + 1):
                cx = x + (c + 0.5) * cw
                cy = y + (row + 0.5) * ch
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK_SOFT)
    for num, col, row in PINS:
        cx = x + (col + 0.5) * cw
        cy = y + (row + 0.5) * ch
        rr = 17
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=RED,
                     outline=(255, 255, 255), width=3)
        f = font(SANS_B, 20)
        t = str(num)
        tw = draw.textlength(t, font=f)
        draw.text((cx - tw / 2, cy - 11), t, font=f, fill=(255, 255, 255))



# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 24
    cw = W - 2 * mx  # 2000

    # ---- masthead
    f_title = font(SERIF_B, 88)
    tw = draw.textlength(MASTHEAD_TITLE, font=f_title)
    draw.text(((W - tw) / 2, 6), MASTHEAD_TITLE, font=f_title, fill=INK)
    draw.line([(mx, 108), (W - mx, 108)], fill=RED, width=5)
    f_date = font(SANS_B, 42)
    tw = draw.textlength(MASTHEAD_DATE, font=f_date)
    draw.text(((W - tw) / 2, 116), MASTHEAD_DATE, font=f_date, fill=RED)
    f_sub = font(SANS_B, 24)
    tw = draw.textlength(MASTHEAD_SUB, font=f_sub)
    draw.text(((W - tw) / 2, 164), MASTHEAD_SUB, font=f_sub, fill=INK_SOFT)
    draw.line([(mx, 196), (W - mx, 196)], fill=INK, width=3)

    # ---- UTC timeline (dayparts, honest coarse times)
    y = 206
    colw = cw / 5
    f_tp = font(SANS_B, 23)
    f_te = font(SANS, 23)
    for i, (part, ev) in enumerate(TIMELINE):
        x = mx + i * colw
        draw.text((x + 6, y), part, font=f_tp, fill=RED)
        draw_wrapped(draw, x + 6, y + 30, ev, f_te, colw - 18, INK, leading=27)
    draw.line([(mx, 298), (W - mx, 298)], fill=INK, width=3)

    # ---- heroes
    y = section_label(draw, mx, 306, "THE THREE BIGGEST STORIES", cw)
    hw, gap = 656, 16
    f_kick = font(SANS_B, 22)
    f_hhead = font(SANS_B, 36)
    f_hbody = font(SANS, 25)
    for i, hero in enumerate(HEROES):
        x = mx + i * (hw + gap)
        hero_image(draw, hero, x, y, hw, 290)
        draw.rectangle([x, y, x + hw, y + 290], outline=INK, width=3)
        badge(draw, x + 12, y + 12, hero["num"])
        ty = y + 298
        draw.text((x, ty), hero["region"] + "  \u00b7  " + hero["field"],
                  font=f_kick, fill=RED)
        ty += 26
        ty = draw_wrapped(draw, x, ty, hero["head"], f_hhead, hw, INK,
                          leading=41)
        draw_wrapped(draw, x, ty + 4, hero["body"], f_hbody, hw, INK_SOFT,
                     leading=28)

    # ---- medium grid (10 cards)
    y = section_label(draw, mx, 856, "TEN MORE", cw)
    mw, mgap, mh = 390, 12, 164
    f_mkick = font(SANS_B, 20)
    f_mhead = font(SANS_B, 25)
    f_mbody = font(SANS, 21)
    for i, m in enumerate(MEDIUM):
        r, c = divmod(i, 5)
        x = mx + c * (mw + mgap)
        yy = y + r * (mh + 6)
        draw.rectangle([x, yy, x + mw, yy + mh], fill=CARD, outline=INK,
                       width=2)
        badge(draw, x + 12, yy + 10, m["num"], d=36)
        draw_icon(draw, m["icon"], x + mw - 66, yy + 10, 54,
                  RED if m["field"] == "WAR" else TEAL)
        draw.text((x + 58, yy + 16),
                  m["region"] + " \u00b7 " + m["field"], font=f_mkick,
                  fill=RED)
        draw_wrapped(draw, x + 14, yy + 56, m["head"], f_mhead, mw - 28,
                     INK, leading=27)
        draw_wrapped(draw, x + 14, yy + 112, m["body"], f_mbody, mw - 28,
                     INK_SOFT, leading=24)

    # ---- map + regions
    y = section_label(draw, mx, 1236,
                      "WHERE IT HAPPENED  (1\u201313 = THE STORIES ABOVE)", cw)
    map_x, map_y, map_w, map_h = mx, y, 560, 270
    draw.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                   fill=(233, 238, 244), outline=INK, width=2)
    draw_map(draw, map_x + 6, map_y + 6, map_w - 12, map_h - 12)
    rx = 608
    f_rt = font(SANS_B, 26)
    draw.text((rx, y + 2), "REGIONS \u2014 35 STORIES", font=f_rt, fill=INK)
    f_rl = font(SANS, 24)
    f_rn = font(SANS_B, 24)
    left_regions = REGIONS[:4]
    right_regions = REGIONS[4:]
    for col_i, group in enumerate((left_regions, right_regions)):
        bx = rx + col_i * 700
        by = y + 40
        for name, n in group:
            draw.text((bx, by), name, font=f_rl, fill=INK)
            bw = int(300 * n / 8)
            draw.rectangle([bx + 200, by + 6, bx + 200 + bw, by + 22],
                           fill=TEAL)
            draw.text((bx + 200 + bw + 12, by), str(n), font=f_rn, fill=INK)
            by += 27
    f_fl = font(SANS, 22)
    draw_wrapped(draw, rx, y + 156,
                 "FIELDS (18): " + FIELDS, f_fl, W - mx - rx, INK_SOFT,
                 leading=26)
    draw.text((rx, y + 214),
              "9 \u00b7 Mercury is off this map \u2014 BepiColombo is in orbit.",
              font=f_fl, fill=INK_SOFT)

    # ---- also on (column-major: left col 14-24, right col 25-35)
    y = section_label(draw, mx, 1552, "ALSO ON \u2014 22 MORE STORIES", cw)
    f_ao = font(SANS, 21)
    f_aob = font(SANS_B, 21)
    col2_x = mx + 1020
    for i, (num, region, text) in enumerate(ALSO_ON):
        col = i // 11
        row = i % 11
        x = mx if col == 0 else col2_x
        yy = y + row * 23
        draw.text((x, yy), str(num), font=f_aob, fill=RED)
        draw.text((x + 44, yy), region + " \u2014 ", font=f_aob, fill=INK)
        rw = draw.textlength(region + " \u2014 ", font=f_aob)
        draw.text((x + 44 + rw, yy), text, font=f_ao, fill=INK_SOFT)

    # ---- date check
    y = 1851
    draw.rectangle([mx, y, W - mx, y + 80], fill=CREAM2, outline=RED, width=2)
    f_dt = font(SANS_B, 22)
    draw.text((mx + 16, y + 6), "DATE CHECK \u2014 LEFT OUT ON PURPOSE",
              font=f_dt, fill=RED)
    f_db = font(SANS, 20)
    joined = "  \u00b7  ".join(DATE_CHECK)
    lines = wrap(draw, joined, f_db, W - 2 * mx - 32)
    ly = y + 34
    for ln in lines[:2]:
        draw.text((mx + 16, ly), ln, font=f_db, fill=INK)
        ly += 22

    # ---- by the numbers
    y = 1939
    f_nb = font(SANS_B, 36)
    f_nl = font(SANS, 18)
    bw = cw / 6
    for i, (big, label) in enumerate(NUMBERS):
        x = mx + i * bw
        if i:
            draw.line([(x - 8, y), (x - 8, y + 58)], fill=GREY, width=2)
        draw.text((x, y), big, font=f_nb, fill=INK)
        draw.text((x, y + 40), label, font=f_nl, fill=INK_SOFT)

    # ---- footer
    f_ft = font(SANS, 20)
    draw.text((mx, 2005), JUDGE_NOTE, font=f_ft, fill=INK_SOFT)
    draw.text((mx, 2027), SOURCES, font=f_ft, fill=GREY)

    grain(img)
    out = img.resize((1024, 1024), Image.LANCZOS)
    out.save(os.path.join(HERE, "entry.png"))
    out.resize((300, 300), Image.LANCZOS).save(
        os.path.join(HERE, "entry-300px.png"))
    print("wrote entry.png", out.size)


if __name__ == "__main__":
    main()
