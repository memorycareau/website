"""Render a 1080x1080 MemoryCare social post PNG with a theme and layout.

Usage:
  python3 render_post.py --out OUT.png --headline "..." --sub "..." \
      [--theme forest|cream|deep|mint|sand] [--layout left|center|card|bold|band] \
      [--tagline "Their day, made simple."] [--button "Join The Waitlist"] [--note "Link in bio"]

Needs Pillow. Uses Inter if installed, otherwise DejaVu Sans.
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo.png")
INTER = "/usr/share/fonts/opentype/inter/"
DEJAVU = "/usr/share/fonts/truetype/dejavu/"
K = 2
S = 1080
PAD = 96


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# bg gradient top/bottom, circle colour+alpha, headline, sub, tagline/brand name, button bg, button text, note, accent
THEMES = {
    "forest": dict(top="#1a7a60", bot="#1f5c4c", circ=(255, 255, 255), ca=(0.08, 0.06), h="#ffffff", sub="#d5eee5",
                   name="#ffffff", tag="#d5eee5", btn="#ffffff", btxt="#1a7a60", note="#ffffff", accent="#d5eee5", card="#ffffff"),
    "cream": dict(top="#f6fbf8", bot="#e1f2ea", circ=(26, 122, 96), ca=(0.07, 0.05), h="#14463a", sub="#3d6b5e",
                  name="#14463a", tag="#3d6b5e", btn="#1a7a60", btxt="#ffffff", note="#14463a", accent="#1a7a60", card="#ffffff"),
    "deep": dict(top="#14433b", bot="#0b2824", circ=(127, 216, 184), ca=(0.10, 0.07), h="#ffffff", sub="#b5e3d1",
                 name="#ffffff", tag="#7fd8b8", btn="#7fd8b8", btxt="#0b2824", note="#ffffff", accent="#7fd8b8", card="#ffffff"),
    "mint": dict(top="#cdeade", bot="#b4dfcd", circ=(255, 255, 255), ca=(0.35, 0.25), h="#0f3f33", sub="#245748",
                 name="#0f3f33", tag="#245748", btn="#0f3f33", btxt="#ffffff", note="#0f3f33", accent="#1a7a60", card="#ffffff"),
    "sand": dict(top="#fcf7ee", bot="#f3e9d6", circ=(232, 160, 90), ca=(0.14, 0.10), h="#1f5c4c", sub="#4b6b5f",
                 name="#1f5c4c", tag="#6a7f74", btn="#1a7a60", btxt="#ffffff", note="#1f5c4c", accent="#e8a05a", card="#ffffff"),
}


def load_font(inter_name, dejavu_name, size):
    for path in (INTER + inter_name, DEJAVU + dejavu_name):
        if os.path.exists(path):
            return ImageFont.truetype(path, size * K)
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--headline", required=True)
    ap.add_argument("--sub", required=True)
    ap.add_argument("--theme", default="forest", choices=THEMES)
    ap.add_argument("--layout", default="left", choices=["left", "center", "card", "bold", "band"])
    ap.add_argument("--tagline", default="Their day, made simple.")
    ap.add_argument("--button", default="Join The Waitlist")
    ap.add_argument("--note", default="Link in bio")
    a = ap.parse_args()
    T = {k: (hexrgb(v) if isinstance(v, str) else v) for k, v in THEMES[a.theme].items()}
    W = S * K

    # background
    img = Image.new("RGB", (W, W))
    px = ImageDraw.Draw(img)
    for y in range(W):
        t = y / (W - 1)
        px.line([(0, y), (W, y)], fill=tuple(round(T["top"][i] + (T["bot"][i] - T["top"][i]) * t) for i in range(3)))
    ov = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    c = T["circ"]
    if a.layout in ("left", "card", "band"):
        od.ellipse([660 * K, -200 * K, 1300 * K, 440 * K], fill=c + (round(255 * T["ca"][0]),))
        od.ellipse([-200 * K, 640 * K, 500 * K, 1340 * K], fill=c + (round(255 * T["ca"][1]),))
    elif a.layout == "center":
        od.ellipse([140 * K, 300 * K, 940 * K, 1100 * K], fill=c + (round(255 * T["ca"][0]),))
        od.ellipse([-260 * K, -260 * K, 300 * K, 300 * K], fill=c + (round(255 * T["ca"][1]),))
        od.ellipse([800 * K, 820 * K, 1300 * K, 1320 * K], fill=c + (round(255 * T["ca"][1]),))
    else:  # bold
        od.ellipse([520 * K, -420 * K, 1400 * K, 460 * K], fill=c + (round(255 * T["ca"][0]),))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)

    def adv(f, s, i):
        ch = s[i]
        if i + 1 < len(s):
            return f.getlength(ch + s[i + 1]) - f.getlength(s[i + 1])
        return f.getlength(ch)

    def tw(s, f, ls=0.0):
        return f.getlength(s) if ls == 0 else sum(adv(f, s, i) + ls for i in range(len(s)))

    def line(x, top_y, lh, s, f, fill, ls=0.0, center=False):
        asc, desc = f.getmetrics()
        base = top_y + (lh - (asc + desc)) / 2 + asc
        if center:
            x = x - tw(s, f, ls) / 2
        if ls == 0:
            d.text((x, base), s, font=f, fill=fill, anchor="ls")
            return
        cx = x
        for i, ch in enumerate(s):
            d.text((cx, base), ch, font=f, fill=fill, anchor="ls")
            cx += adv(f, s, i) + ls

    def wrap(s, f, max_w, ls=0.0):
        lines, cur = [], ""
        for w in s.split(" "):
            t = (cur + " " + w).strip()
            if tw(t, f, ls) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        return lines

    logo = Image.open(LOGO).convert("RGBA")

    def paste_logo(x, y, size):
        lg = logo.resize((size * K, size * K), Image.LANCZOS)
        m = Image.new("L", lg.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, size * K - 1, size * K - 1], radius=round(size * 0.25) * K, fill=255)
        img.paste(lg, (x * K, y * K), Image.composite(lg.split()[3], Image.new("L", lg.size, 0), m))

    f_name = load_font("Inter-Bold.otf", "DejaVuSans-Bold.ttf", 40)
    f_tag = load_font("Inter-Regular.otf", "DejaVuSans.ttf", 24)

    def header_left(x, y, name_col=None, tag_col=None):
        paste_logo(x, y, 88)
        tx = x + 88 + 20
        ty = y + (88 - 84) / 2
        line(tx * K, ty * K, 48 * K, "MemoryCare", f_name, name_col or T["name"])
        line(tx * K, (ty + 52) * K, 32 * K, a.tagline, f_tag, tag_col or T["tag"])

    def fit(max_w, avail, start, ls_k=-0.02, sub_w=800, sub_size=38, sub_lh=54, gap=32, lh_k=1.1, minsize=48, weight="Inter-ExtraBold.otf"):
        size = start
        while True:
            fh = load_font(weight, "DejaVuSans-Bold.ttf", size)
            ls = ls_k * size * K
            h1 = wrap(a.headline, fh, max_w * K, ls)
            lh = round(size * lh_k)
            fp = load_font("Inter-Regular.otf", "DejaVuSans.ttf", sub_size)
            p = wrap(a.sub, fp, sub_w * K)
            total = len(h1) * lh + gap + len(p) * sub_lh
            if total <= avail or size <= minsize:
                return fh, ls, h1, lh, fp, p, total
            size -= 4

    f_b = load_font("Inter-Bold.otf", "DejaVuSans-Bold.ttf", 40)
    f_n = load_font("Inter-SemiBold.otf", "DejaVuSans-Bold.ttf", 32)
    bw = tw(a.button, f_b) / K + 88

    def button(x, y, btn=None, btxt=None, note=None):
        d.rounded_rectangle([x * K, y * K, (x + bw) * K, (y + 96) * K], radius=48 * K, fill=btn or T["btn"])
        line((x + 44) * K, y * K, 96 * K, a.button, f_b, btxt or T["btxt"])
        if a.note:
            line((x + bw + 24) * K, (y + 28) * K, 40 * K, a.note, f_n, note or T["note"])

    if a.layout == "left":
        header_left(PAD, PAD)
        avail = S - 2 * PAD - 88 - 96 - 40
        fh, ls, h1, lh, fp, p, total = fit(S - 2 * PAD, avail, 80)
        y = PAD + 88 + (S - 2 * PAD - 88 - 96 - total) / 2
        for ln in h1:
            line(PAD * K, y * K, lh * K, ln, fh, T["h"], ls)
            y += lh
        y += 32
        for ln in p:
            line(PAD * K, y * K, 54 * K, ln, fp, T["sub"])
            y += 54
        button(PAD, S - PAD - 96)

    elif a.layout == "center":
        # logo centred on top, centred text, centred button; note underneath
        paste_logo(S // 2 - 52, PAD - 8, 104)
        line(S / 2 * K, (PAD + 104) * K, 48 * K, "MemoryCare", f_name, T["name"], center=True)
        line(S / 2 * K, (PAD + 104 + 48) * K, 32 * K, a.tagline, f_tag, T["tag"], center=True)
        top = PAD + 104 + 100
        avail = S - top - PAD - 96 - 40 - 60
        fh, ls, h1, lh, fp, p, total = fit(S - 2 * PAD - 40, avail, 84, sub_w=780)
        y = top + (avail - total) / 2 + 20
        for ln in h1:
            line(S / 2 * K, y * K, lh * K, ln, fh, T["h"], ls, center=True)
            y += lh
        y += 32
        for ln in p:
            line(S / 2 * K, y * K, 54 * K, ln, fp, T["sub"], center=True)
            y += 54
        by = S - PAD - 96 - 44
        d.rounded_rectangle([(S - bw) / 2 * K, by * K, (S + bw) / 2 * K, (by + 96) * K], radius=48 * K, fill=T["btn"])
        line(S / 2 * K, by * K, 96 * K, a.button, f_b, T["btxt"], center=True)
        if a.note:
            line(S / 2 * K, (by + 96 + 8) * K, 40 * K, a.note, f_n, T["note"], center=True)

    elif a.layout == "card":
        header_left(PAD, 72)
        inner = 64 + 64
        by = S - 72 - 96
        zone_top, zone_bot = 72 + 88 + 36, by - 36
        fh, ls, h1, lh, fp, p, total = fit(S - 2 * inner, zone_bot - zone_top - 2 * 72, 96, sub_w=S - 2 * inner, minsize=56)
        ch = total + 2 * 72 + 24
        card_top = zone_top + (zone_bot - zone_top - ch) / 2
        card_bot = card_top + ch
        d.rounded_rectangle([64 * K, card_top * K, (S - 64) * K, card_bot * K], radius=48 * K, fill=T["card"])
        y = card_top + 72 + 24
        d.rounded_rectangle([inner * K, (card_top + 48) * K, (inner + 72) * K, (card_top + 60) * K], radius=6 * K, fill=hexrgb("#1a7a60"))
        for ln in h1:
            line(inner * K, y * K, lh * K, ln, fh, hexrgb("#14463a"), ls)
            y += lh
        y += 32
        for ln in p:
            line(inner * K, y * K, 54 * K, ln, fp, hexrgb("#3d6b5e"))
            y += 54
        button(64, by)

    elif a.layout == "bold":
        # small header top-left, huge headline anchored low, thin accent rule, button bottom
        header_left(PAD, PAD)
        avail = 560
        fh, ls, h1, lh, fp, p, total = fit(S - 2 * PAD, avail, 112, ls_k=-0.03, sub_w=820, sub_size=36, sub_lh=50, gap=36, lh_k=1.04, minsize=56)
        by = S - PAD - 96
        y_end = by - 56
        y = y_end - total
        for ln in h1:
            line(PAD * K, y * K, lh * K, ln, fh, T["h"], ls)
            y += lh
        y += 36
        d.rounded_rectangle([PAD * K, (y - 20) * K, (PAD + 96) * K, (y - 12) * K], radius=4 * K, fill=T["accent"])
        y += 12
        for ln in p:
            line(PAD * K, y * K, 50 * K, ln, fp, T["sub"])
            y += 50
        button(PAD, by)

    else:  # band
        band_h = 232
        d.rectangle([0, 0, W, band_h * K], fill=T["btn"] if a.theme != "forest" else hexrgb("#14463a"))
        on_band_name = T["btxt"] if a.theme != "forest" else hexrgb("#ffffff")
        on_band_tag = T["btxt"] if a.theme != "forest" else hexrgb("#d5eee5")
        header_left(PAD, (band_h - 88) // 2, on_band_name, on_band_tag)
        top = band_h
        avail = S - top - PAD - 96 - 40 - 40
        fh, ls, h1, lh, fp, p, total = fit(S - 2 * PAD, avail, 84)
        y = top + 56 + (avail - total) / 2
        for ln in h1:
            line(PAD * K, y * K, lh * K, ln, fh, T["h"], ls)
            y += lh
        y += 32
        for ln in p:
            line(PAD * K, y * K, 54 * K, ln, fp, T["sub"])
            y += 54
        button(PAD, S - PAD - 96)

    img.convert("RGB").resize((S, S), Image.LANCZOS).save(a.out, optimize=True)
    print("saved", a.out)


if __name__ == "__main__":
    main()
