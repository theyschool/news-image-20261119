#!/usr/bin/env python3
"""Render the news-image-20261119 poster: 'THE WORLD IN ONE DAY',
Thursday 19 November 2026. All text is drawn with real fonts
(Liberation Serif/Sans); every illustration is drawn with PIL
primitives. No AI-generated imagery, no network. Deterministic:
same input, same bytes out.

Stories, all verified as 19 November 2026 events or first reports:
  lead  Trump, Xi and Putin meet in Shenzhen (Reuters, 18 Nov;
        meeting held Thursday 19 Nov, APEC sidelines)
  law   ICJ rules on Rohingya genocide case (Le Monde, 19 Nov;
        judgment read 10:00 CET, The Hague)
  games GTA VI launches worldwide (Rockstar; rolling midnight
        launch 19 Nov; live in NZ/Australia/Asia by 00:00 UTC)
  storm Cyclone Akvan nears India's east coast (IMD bulletin
        02:30 IST, 19 Nov; red alert, landfall due 20 Nov)
  money Wall Street falls for a fifth day (19 Nov morning
        market reports; Dow -1.3%, gold and copper tumble)
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (26, 26, 26)
NAVY = (15, 42, 74)
GOLD = (232, 184, 75)
RED = (185, 28, 28)
GREEN = (46, 125, 50)
GRAY = (110, 110, 105)
RULE = (200, 192, 178)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_tracked(draw, xy, s, f, fill, tracking=0):
    """Draw text with manual letter tracking (PIL has no tracking)."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def draw_centered(draw, cx, y, s, f, fill, tracking=0):
    w = sum(draw.textlength(ch, font=f) + tracking for ch in s) - tracking
    draw_tracked(draw, (cx - w / 2, y), s, f, fill, tracking)
    return w


def wrap(draw, s, f, max_w):
    """Greedy word wrap to lines fitting max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- illustrations
# Every picture is drawn from primitives: flat colour, bold shapes, no text.

def ill_shenzhen(draw, box):
    """Summit: Shenzhen towers at dawn, a tall spire, three flags."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(232, 222, 190))
    # sun
    sx, sy = x0 + int(w * 0.74), y0 + int(h * 0.22)
    draw.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], fill=GOLD)
    # skyline silhouettes
    base = y0 + int(h * 0.86)
    towers = [(0.03, 0.50), (0.19, 0.68), (0.35, 0.42), (0.51, 0.60),
              (0.80, 0.56)]
    for fx, fh in towers:
        tx0 = x0 + int(w * fx)
        tw = int(w * 0.13)
        th = int(h * fh)
        draw.rectangle([tx0, base - th, tx0 + tw, base], fill=(38, 52, 74))
    # tall spire rising above the rest
    px = x0 + int(w * 0.64)
    draw.polygon([(px - 8, base), (px, y0 + int(h * 0.05)), (px + 8, base)],
                 fill=NAVY)
    draw.rectangle([x0, base, x1, y1], fill=(38, 52, 74))
    # lit windows
    for wx, wy in ((0.08, 0.58), (0.24, 0.50), (0.40, 0.66), (0.56, 0.56),
                   (0.85, 0.64)):
        draw.rectangle([x0 + int(w * wx), y0 + int(h * wy),
                        x0 + int(w * wx) + 5, y0 + int(h * wy) + 5],
                       fill=GOLD)
    # three flags on poles above the ground line
    for i, col in enumerate((RED, (46, 90, 136), (220, 220, 220))):
        fx = x0 + int(w * (0.22 + i * 0.26))
        fy = y0 + int(h * 0.70)
        draw.line([(fx, fy), (fx, fy - 34)], fill=INK, width=3)
        draw.polygon([(fx, fy - 34), (fx + 26, fy - 28), (fx, fy - 22)],
                     fill=col)


def ill_scales(draw, box):
    """Law: scales of justice over a courthouse pediment."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(224, 232, 240))
    cx = x0 + w // 2
    # pediment
    draw.polygon([(x0 + int(w * 0.12), y0 + int(h * 0.30)),
                  (cx, y0 + int(h * 0.14)),
                  (x1 - int(w * 0.12), y0 + int(h * 0.30))], fill=NAVY)
    # columns
    for fx in (0.20, 0.42, 0.58, 0.80):
        px = x0 + int(w * fx)
        draw.rectangle([px - 9, y0 + int(h * 0.32), px + 9,
                        y0 + int(h * 0.62)], fill=(255, 255, 255))
    draw.rectangle([x0 + int(w * 0.10), y0 + int(h * 0.62),
                    x1 - int(w * 0.10), y0 + int(h * 0.68)], fill=NAVY)
    # scales, hanging in front, lower half
    cy = y0 + int(h * 0.80)
    draw.line([(cx, y0 + int(h * 0.66)), (cx, cy)], fill=INK, width=4)
    draw.line([(cx - 52, cy - 8), (cx + 52, cy - 8)], fill=INK, width=4)
    for sgn in (-1, 1):
        bx = cx + sgn * 52
        draw.line([(bx, cy - 8), (bx - 20, cy + 26)], fill=INK, width=3)
        draw.line([(bx, cy - 8), (bx + 20, cy + 26)], fill=INK, width=3)
        draw.pieslice([bx - 22, cy + 22, bx + 22, cy + 34], start=0, end=180,
                      fill=GOLD)
    draw.ellipse([cx - 6, cy - 14, cx + 6, cy - 2], fill=INK)


def ill_vicecity(draw, box):
    """Gaming: neon sunset, palm trees and a low car in Vice City."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # dusk sky
    draw.rectangle(box, fill=(24, 18, 48))
    cx, cy = x0 + w // 2, y0 + int(h * 0.44)
    r = int(min(w, h) * 0.30)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 90))
    # sun stripes
    for i, yy in enumerate((0.52, 0.58, 0.64)):
        y = y0 + int(h * yy)
        draw.rectangle([cx - r, y, cx + r, y + 5], fill=(24, 18, 48))
    # sea strip
    draw.rectangle([x0, y0 + int(h * 0.72), x1, y1], fill=(16, 60, 90))
    # palms
    def palm(px, py, s, lean):
        draw.line([(px, py), (px + lean, py - 46 * s)], fill=(10, 40, 20),
                  width=max(3, int(5 * s)))
        top = (px + lean, py - 46 * s)
        for ang in (-150, -110, -70, -30, 10):
            a = math.radians(ang)
            ex = top[0] + int(30 * s * math.cos(a))
            ey = top[1] + int(16 * s * math.sin(a)) - 6
            draw.line([top, (ex, ey)], fill=(10, 40, 20),
                      width=max(2, int(3 * s)))
    palm(x0 + int(w * 0.16), y0 + int(h * 0.74), 1.0, 8)
    palm(x0 + int(w * 0.86), y0 + int(h * 0.76), 0.85, -8)
    # low sports car, side profile
    jx, jy = x0 + int(w * 0.30), y0 + int(h * 0.80)
    draw.polygon([(jx, jy + 10), (jx + 14, jy), (jx + 62, jy - 2),
                  (jx + 88, jy + 6), (jx + 96, jy + 12), (jx, jy + 14)],
                 fill=(232, 184, 75))
    draw.polygon([(jx + 22, jy), (jx + 34, jy - 10), (jx + 58, jy - 10),
                  (jx + 66, jy - 2)], fill=(38, 52, 74))
    for wx in (jx + 20, jx + 70):
        draw.ellipse([wx - 9, jy + 6, wx + 9, jy + 24], fill=INK)
        draw.ellipse([wx - 4, jy + 11, wx + 4, jy + 19], fill=(200, 200, 200))


def ill_cyclone(draw, box):
    """Weather: cyclone spiral over the sea."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(224, 232, 240))
    cx, cy = x0 + w // 2, y0 + int(h * 0.44)
    # spiral arms
    for start_r, end_r, col, wd in ((8, 62, NAVY, 7), (8, 46, (46, 125, 150), 5)):
        pts = []
        turns = 2.1
        steps = 90
        for i in range(steps + 1):
            t = i / steps
            ang = t * turns * 2 * math.pi
            r = start_r + (end_r - start_r) * t
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.92))
        draw.line(pts, fill=col, width=wd)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=NAVY)
    # sea
    draw.rectangle([x0, y0 + int(h * 0.80), x1, y1], fill=(110, 168, 205))
    for wy in (0.86, 0.92):
        yy = y0 + int(h * wy)
        draw.line([(x0 + 10, yy), (x1 - 10, yy)], fill=(255, 255, 255), width=3)
    # rain drops
    for dx, dy in ((-52, -56), (48, -64), (64, -32), (-64, -28)):
        draw.ellipse([cx + dx - 3, cy + dy - 6, cx + dx + 3, cy + dy + 6],
                     fill=(46, 125, 150))


def ill_markets(draw, box):
    """Markets: falling bars and a down-trending line."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(240, 224, 224))
    base = y0 + int(h * 0.82)
    # falling bars
    bx = x0 + int(w * 0.14)
    for i, bh in enumerate((66, 56, 44, 30)):
        draw.rectangle([bx + i * 34, base - bh, bx + i * 34 + 24, base],
                       fill=RED)
    # down trend line with arrow
    pts = [(bx - 4, base - 78), (bx + 30, base - 62), (bx + 64, base - 48),
           (bx + 98, base - 34), (bx + 128, base - 18)]
    draw.line(pts, fill=INK, width=5)
    ax, ay = pts[-1]
    draw.polygon([(ax, ay), (ax - 14, ay - 2), (ax - 2, ay + 12)], fill=INK)
    # small uptick at the end, crossed out
    draw.line([(bx + 96, base - 26), (bx + 128, base - 18)], fill=GREEN, width=3)


# ---------------------------------------------------------------- composition

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 172], fill=RED)
    f_kick = font(SANS_BOLD, 25)
    draw_centered(d, W // 2, 24, "T H E   W O R L D   I N   O N E   D A Y",
                  f_kick, GOLD, tracking=2)
    f_date = font(SERIF, 58)
    draw_centered(d, W // 2, 62, "THURSDAY 19 NOVEMBER 2026", f_date,
                  (255, 255, 255))
    d.line([(W // 2 - 330, 140), (W // 2 + 330, 140)], fill=GOLD, width=2)
    f_sub = font(SANS, 21)
    draw_centered(d, W // 2, 146,
                  "Five stories that defined the day  —  from Shenzhen to The Hague to Vice City",
                  f_sub, (200, 214, 228))

    # --- lead story: trilateral in Shenzhen ---
    ill_shenzhen(d, (24, 196, 400, 454))
    d.rectangle([24, 196, 400, 454], outline=INK, width=2)
    tx = 424
    f_lkick = font(SANS_BOLD, 20)
    draw_tracked(d, (tx, 198), "CHINA  •  DIPLOMACY", f_lkick, RED, tracking=1)
    f_lhead = font(SERIF, 45)
    d.text((tx, 226), "TRUMP, XI & PUTIN", font=f_lhead, fill=INK)
    d.text((tx, 272), "MEET IN SHENZHEN", font=f_lhead, fill=INK)
    f_lbody = font(SANS, 23)
    lead = ("The leaders of the world's three largest nuclear powers "
            "meet today in Shenzhen, on the APEC sidelines, with nuclear "
            "arms control on the agenda.")
    y = 330
    for line in wrap(d, lead, f_lbody, 1000 - tx - 8):
        d.text((tx, y), line, font=f_lbody, fill=INK)
        y += 30
    f_lfoot = font(SANS_BOLD, 19)
    d.text((tx, 428), "One hour set aside for the three-way talks",
           font=f_lfoot, fill=GRAY)

    # --- divider ---
    d.line([(24, 478), (1000, 478)], fill=RULE, width=2)

    # --- four stories, 2 x 2 grid ---
    stories = [
        ("LAW  •  THE HAGUE", "ROHINGYA VERDICT",
         "The UN's top court rules today on whether Myanmar committed "
         "genocide against the Rohingya — the first time it could hold "
         "a state responsible.",
         ill_scales, NAVY),
        ("CULTURE  •  GAMING", "GTA VI LAUNCHES",
         "Rockstar's blockbuster goes on sale today, at midnight in "
         "each country, 13 years after GTA V; pre-orders top $1.5bn.",
         ill_vicecity, RED),
        ("WEATHER  •  INDIA", "AKVAN NEARS",
         "The severe cyclone bears down on India's east coast; a red "
         "alert is in force as heavy rain hits Andhra Pradesh and "
         "Odisha. Landfall is due on Friday.",
         ill_cyclone, (15, 90, 120)),
        ("MARKETS  •  GLOBAL", "STOCKS SLIDE",
         "Wall Street falls for a fifth straight day; the Dow drops "
         "1.3% as gold and copper tumble and Fed minutes point to "
         "more rate rises.",
         ill_markets, RED),
    ]
    f_ckick = font(SANS_BOLD, 18)
    f_chead = font(SERIF, 31)
    f_cbody = font(SANS, 20)
    cell_w, cell_h = 476, 236
    for i, (kick, head, body, ill, col) in enumerate(stories):
        cx0 = 24 + (i % 2) * (cell_w + 24)
        cy0 = 496 + (i // 2) * (cell_h + 16)
        # illustration, left
        ill(d, (cx0, cy0, cx0 + 168, cy0 + 168))
        d.rectangle([cx0, cy0, cx0 + 168, cy0 + 168], outline=INK, width=2)
        tx2 = cx0 + 184
        tw = cx0 + cell_w - tx2
        draw_tracked(d, (tx2, cy0 + 2), kick, f_ckick, col, tracking=1)
        # shrink the headline until it fits the text column
        f_head = f_chead
        size = 31
        while d.textlength(head, font=f_head) > tw and size > 22:
            size -= 1
            f_head = font(SERIF, size)
        d.text((tx2, cy0 + 28), head, font=f_head, fill=INK)
        y = cy0 + 70
        for line in wrap(d, body, f_cbody, tw):
            d.text((tx2, y), line, font=f_cbody, fill=INK)
            y += 26

    # --- footer ---
    d.line([(24, 984), (1000, 984)], fill=RULE, width=2)
    f_foot = font(SANS, 16)
    draw_centered(d, W // 2, 992,
                  "Sources: Reuters, Le Monde, Associated Press, India Meteorological Department  •  19 November 2026",
                  f_foot, GRAY)
    return img


if __name__ == "__main__":
    render().save("entry.png", "PNG")
    print("wrote entry.png")
