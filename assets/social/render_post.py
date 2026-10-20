"""Render a 1080x1080 MemoryCare social post PNG.

Usage:
  python3 assets/social/render_post.py --out assets/social/memorycare-YYYY-MM-DD.png \
      --headline "One step at a time." \
      --sub "Offer one simple step, stay calm, and give time to respond." \
      --tagline "Their day, made simple." \
      --button "Join The Waitlist" --note "Link in bio"

Needs Pillow. Uses Inter if installed, otherwise DejaVu Sans.
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo.png")
INTER = "/usr/share/fonts/opentype/inter/"
DEJAVU = "/usr/share/fonts/truetype/dejavu/"
K = 2  # supersample factor


def load_font(inter_name, dejavu_name, size):
    for path in (INTER + inter_name, DEJAVU + dejavu_name):
        if os.path.exists(path):
            return ImageFont.truetype(path, size * K)
    return ImageFont.load_default()


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--headline", required=True)
    ap.add_argument("--sub", required=True)
    ap.add_argument("--tagline", default="Their day, made simple.")
    ap.add_argument("--button", default="Join The Waitlist")
    ap.add_argument("--note", default="Link in bio")
    a = ap.parse_args()

    W = 1080 * K
    PAD = 96
    WHITE, TRACK, BRAND = (255, 255, 255), hexrgb("#d5eee5"), hexrgb("#1a7a60")

    img = Image.new("RGB", (W, W))
    top, bot = hexrgb("#1a7a60"), hexrgb("#1f5c4c")
    px = ImageDraw.Draw(img)
    for y in range(W):
        t = y / (W - 1)
        px.line([(0, y), (W, y)], fill=tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    ov = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse([660 * K, -200 * K, 1300 * K, 440 * K], fill=(255, 255, 255, round(255 * 0.08)))
    od.ellipse([-200 * K, 640 * K, 500 * K, 1340 * K], fill=(255, 255, 255, round(255 * 0.06)))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)

    def adv(f, s, i):
        c = s[i]
        if i + 1 < len(s):
            return f.getlength(c + s[i + 1]) - f.getlength(s[i + 1])
        return f.getlength(c)

    def text_w(s, f, ls=0.0):
        if ls == 0:
            return f.getlength(s)
        return sum(adv(f, s, i) + ls for i in range(len(s)))

    def draw_line(x, top_y, line_h, s, f, fill, ls=0.0):
        asc, desc = f.getmetrics()
        base = top_y + (line_h - (asc + desc)) / 2 + asc
        if ls == 0:
            d.text((x, base), s, font=f, fill=fill, anchor="ls")
            return
        cx = x
        for i, c in enumerate(s):
            d.text((cx, base), c, font=f, fill=fill, anchor="ls")
            cx += adv(f, s, i) + ls

    def wrap(s, f, max_w, ls=0.0):
        lines, cur = [], ""
        for w in s.split(" "):
            t = (cur + " " + w).strip()
            if text_w(t, f, ls) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        return lines

    # header: logo + name + tagline
    logo = Image.open(LOGO).convert("RGBA").resize((88 * K, 88 * K), Image.LANCZOS)
    mask = Image.new("L", logo.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 88 * K - 1, 88 * K - 1], radius=22 * K, fill=255)
    img.paste(logo, (PAD * K, PAD * K), Image.composite(logo.split()[3], Image.new("L", logo.size, 0), mask))
    d = ImageDraw.Draw(img)
    tx = (PAD + 88 + 20) * K
    ty = PAD + (88 - 84) / 2
    draw_line(tx, ty * K, 48 * K, "MemoryCare", load_font("Inter-Bold.otf", "DejaVuSans-Bold.ttf", 40), WHITE)
    draw_line(tx, (ty + 52) * K, 32 * K, a.tagline, load_font("Inter-Regular.otf", "DejaVuSans.ttf", 24), TRACK)

    # headline + supporting line, fitted to the available height
    avail = 1080 - 2 * PAD - 88 - 96
    size = 80
    while True:
        f_h1 = load_font("Inter-ExtraBold.otf", "DejaVuSans-Bold.ttf", size)
        ls = -0.02 * size * K
        h1 = wrap(a.headline, f_h1, (1080 - 2 * PAD) * K, ls)
        lh = round(size * 1.1)
        f_p = load_font("Inter-Regular.otf", "DejaVuSans.ttf", 38)
        p = wrap(a.sub, f_p, 800 * K)
        mid_h = len(h1) * lh + 32 + len(p) * 54
        if mid_h <= avail - 40 or size <= 48:
            break
        size -= 4
    y = PAD + 88 + (avail - mid_h) / 2
    for ln in h1:
        draw_line(PAD * K, y * K, lh * K, ln, f_h1, WHITE, ls)
        y += lh
    y += 32
    for ln in p:
        draw_line(PAD * K, y * K, 54 * K, ln, f_p, TRACK)
        y += 54

    # bottom row: button + note
    f_b = load_font("Inter-Bold.otf", "DejaVuSans-Bold.ttf", 40)
    bw = text_w(a.button, f_b) / K + 88
    by = 1080 - PAD - 96
    d.rounded_rectangle([PAD * K, by * K, (PAD + bw) * K, (by + 96) * K], radius=48 * K, fill=WHITE)
    draw_line((PAD + 44) * K, by * K, 96 * K, a.button, f_b, BRAND)
    if a.note:
        draw_line((PAD + bw + 24) * K, (by + 28) * K, 40 * K, a.note,
                  load_font("Inter-SemiBold.otf", "DejaVuSans-Bold.ttf", 32), WHITE)

    img.convert("RGB").resize((1080, 1080), Image.LANCZOS).save(a.out, optimize=True)
    print("saved", a.out)


if __name__ == "__main__":
    main()
