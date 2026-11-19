#!/usr/bin/env python3
"""Draw the newspaper front page for Thursday 19 November 2026.

Renders 'The World in One Day' as a 1024x1024 PNG poster with five
stories, all verified 19 November 2026 events. Every word is drawn with
a real font (Liberation Serif / Liberation Sans) and every picture is a
PIL primitive, so no text is ever garbled. The output is deterministic:
running this script twice produces byte-identical PNG bytes.
"""

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 48
PAPER = (247, 243, 232)
INK = (18, 18, 18)
GREY = (90, 86, 76)
RED = (148, 24, 24)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF = FONT_DIR + "LiberationSerif-Regular.ttf"
SERIF_BOLD = FONT_DIR + "LiberationSerif-Bold.ttf"
SERIF_ITALIC = FONT_DIR + "LiberationSerif-Italic.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"
SANS_BOLD = FONT_DIR + "LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill=INK, leading=1.35):
    """Draw wrapped paragraph text; returns the y after the last line."""
    line_h = int(fnt.size * leading)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def draw_centred(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """A simple globe motif: circle, meridians, parallels, three dots."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    # meridians
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=INK, width=2)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=INK, width=2)
    # parallels
    for dy in (-r // 2, r // 2):
        half = int((r * r - dy * dy) ** 0.5)
        draw.line([(cx - half, cy + dy), (cx + half, cy + dy)], fill=INK, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=2)
    # three leaders: two dots flanking the globe
    for dx, dy in ((-r - 16, -r // 2), (r + 16, -r // 2)):
        draw.ellipse([cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6],
                     fill=RED)


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    d = ImageDraw.Draw(img)
    content_w = WIDTH - 2 * MARGIN
    x0 = MARGIN
    x1 = WIDTH - MARGIN

    # ---- Masthead -------------------------------------------------
    y = 40
    rule(d, x0, y, x1, width=3)
    y += 22
    name_f = font(SERIF_BOLD, 74)
    y = draw_centred(d, WIDTH // 2, y, "The World in One Day", name_f)
    y += 14
    date_f = font(SANS_BOLD, 28)
    date_text = "THURSDAY  19  NOVEMBER  2026"
    dw = d.textlength(date_text, font=date_f)
    rule(d, x0, y + 15, (WIDTH - dw) // 2 - 18, width=2)
    rule(d, (WIDTH + dw) // 2 + 18, y + 15, x1, width=2)
    draw_centred(d, WIDTH // 2, y, date_text, date_f, fill=RED)
    y += 28 + 20
    rule(d, x0, y, x1, width=4)
    y += 26

    # ---- Lead story: THREE LEADERS, ONE TABLE ---------------------
    head_f = font(SERIF_BOLD, 56)
    body_f = font(SANS, 24)
    lead_head = "THREE LEADERS, ONE TABLE"
    hw = d.textlength(lead_head, font=head_f)
    if hw > content_w:
        head_f = font(SERIF_BOLD, 48)
    y = draw_centred(d, WIDTH // 2, y, lead_head, head_f)
    y += 18
    # globe motif at the right of the lead body
    globe_r = 56
    globe_cx = x1 - globe_r - 8
    globe_cy = y + 68
    lead_text = (
        "Donald Trump, Xi Jinping and Vladimir Putin meet in Shenzhen "
        "at the APEC summit today, the first time the three leaders "
        "have sat down together at one table. Trade, the war in "
        "Ukraine and the future of the Pacific top the agenda as the "
        "world watches the summit open."
    )
    body_w = content_w - (globe_r * 2 + 30)
    y = draw_wrapped(d, x0, y, lead_text, body_f, body_w, leading=1.4)
    draw_globe(d, globe_cx, globe_cy, globe_r)
    draw_centred(d, globe_cx, globe_cy + globe_r + 14, "SHENZHEN",
                 font(SANS_BOLD, 14), fill=GREY)
    y += 34
    rule(d, x0, y, x1, width=2)
    y += 26

    # ---- Middle row: two stories ----------------------------------
    col_gap = 36
    col_w = (content_w - col_gap) // 2
    mid_top = y
    sub_head_f = font(SERIF_BOLD, 33)
    sub_body_f = font(SANS, 21)

    # Left: ROHINGYA RULING
    ly = mid_top
    ly = draw_wrapped(d, x0, ly, "ROHINGYA RULING", sub_head_f, col_w)
    ly += 6
    ly = draw_wrapped(
        d, x0, ly,
        "The International Court of Justice in The Hague hands down "
        "its ruling on the Rohingya case, a landmark decision for "
        "the people of Myanmar.",
        sub_body_f, col_w, leading=1.4)

    # Right: GTA VI LAUNCHES
    rx = x0 + col_w + col_gap
    ry = mid_top
    ry = draw_wrapped(d, rx, ry, "GTA VI LAUNCHES", sub_head_f, col_w)
    ry += 6
    ry = draw_wrapped(
        d, rx, ry,
        "Grand Theft Auto VI releases worldwide on a rolling midnight "
        "unlock, the biggest entertainment launch of the year. "
        "Players return to Leonida.",
        sub_body_f, col_w, leading=1.4)

    y = max(ly, ry) + 24
    rule(d, x0, y, x1, width=2)
    y += 26

    # ---- Bottom row: two stories ----------------------------------
    bot_top = y
    # Left: CYCLONE AKVAN
    ly = bot_top
    ly = draw_wrapped(d, x0, ly, "CYCLONE AKVAN", sub_head_f, col_w)
    ly += 6
    ly = draw_wrapped(
        d, x0, ly,
        "The storm sits about 480 km south-east of Narsapur with a "
        "red alert on India's east coast. Landfall is expected on "
        "Friday as coastal districts prepare.",
        sub_body_f, col_w, leading=1.4)

    # Right: MARKETS SLIDE
    ry = bot_top
    ry = draw_wrapped(d, rx, ry, "MARKETS SLIDE", sub_head_f, col_w)
    ry += 6
    ry = draw_wrapped(
        d, rx, ry,
        "US stocks fall for a fifth straight session. The Dow drops "
        "1.3% after the Fed minutes, and investors brace for more "
        "volatility ahead.",
        sub_body_f, col_w, leading=1.4)

    y = max(ly, ry) + 28
    rule(d, x0, y, x1, width=3)
    y += 20
    # contents line: where each story lives
    contents_f = font(SANS_BOLD, 19)
    contents = "INSIDE:  SHENZHEN SUMMIT  ·  THE HAGUE  ·  LEONIDA  ·  NARSAPUR  ·  WALL STREET"
    draw_centred(d, WIDTH // 2, y, contents, contents_f, fill=GREY)
    y += 30
    rule(d, x0, y, x1, width=2)
    y += 18
    foot_f = font(SERIF_ITALIC, 19)
    draw_centred(
        d, WIDTH // 2, y,
        "The World in One Day  —  Thursday 19 November 2026  —  Five stories that defined the day.",
        foot_f, fill=GREY)

    img.save("entry.png", format="PNG")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
