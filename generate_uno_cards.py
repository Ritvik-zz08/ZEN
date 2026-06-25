#!/usr/bin/env python3
"""
Generate all 54 unique UNO card images for use as Discord custom emojis.
Run ONCE locally (or let the bot run it automatically on startup):

    python generate_uno_cards.py

Output: assets/uno_cards/*.png  (90×128 px transparent-background PNGs)
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "uno_cards")
os.makedirs(OUT, exist_ok=True)

W, H = 90, 128   # portrait card – works fine as Discord emoji

# ── Colour palette ────────────────────────────────────────────────────────────
PALETTE = {
    "red":    ("#E74C3C", "#922B21"),
    "blue":   ("#2E86DE", "#1A5276"),
    "green":  ("#27AE60", "#1E8449"),
    "yellow": ("#F4D03F", "#9A7D0A"),
}
WILD_QUADS = ["#E74C3C", "#2E86DE", "#27AE60", "#F4D03F"]

# ── Font helper (works on Windows, Linux/Render, macOS) ──────────────────────
_FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",          # Render / Debian
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",   # Ubuntu
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",                    # RHEL
    "C:/Windows/Fonts/arialbd.ttf",                                    # Windows
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",                             # macOS
]

def _font(size: int) -> ImageFont.FreeTypeFont:
    for p in _FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default(size=size)   # Pillow 10+
    except TypeError:
        return ImageFont.load_default()

def _center_text(draw, text, font, cx, cy, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((cx - w / 2, cy - h / 2), text, fill=fill, font=font)

# ── Card builders ─────────────────────────────────────────────────────────────
def make_color_card(filename: str, bg: str, dark: str, label: str):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Card body with rounded corners
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=12,
                         fill=bg, outline=dark, width=5)

    # Inner white oval
    d.ellipse([10, 20, W - 10, H - 20], fill="white")

    # Centre value (large, in card colour so it "pops")
    f_big = _font(34)
    _center_text(d, label, f_big, W // 2, H // 2, bg)

    # Top-left corner value (small, white)
    f_sm = _font(14)
    d.text((6, 5), label, fill="white", font=f_sm)

    img.save(os.path.join(OUT, filename))
    print(f"  [ok] {filename}")

def make_wild_card(filename: str, plus4: bool):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Black card body
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=12,
                         fill="#111111", outline="#333333", width=4)

    # Four coloured ovals (quadrant style — classic Wild look)
    cx, cy, r = W // 2, H // 2, 26
    offsets = [(-r // 2, -r // 2), (r // 2, -r // 2),
               (-r // 2,  r // 2), (r // 2,  r // 2)]
    for (ox, oy), c in zip(offsets, WILD_QUADS):
        d.ellipse([cx + ox - r, cy + oy - r,
                   cx + ox + r, cy + oy + r], fill=c)

    # Dark centre cutout
    d.ellipse([cx - 18, cy - 26, cx + 18, cy + 26], fill="#111111")

    # Centre label
    label = "+4" if plus4 else "W"
    f = _font(22)
    _center_text(d, label, f, cx, cy, "white")

    # Small corner text
    f_sm = _font(12)
    corner_label = "W+4" if plus4 else "W"
    d.text((5, 5), corner_label, fill="white", font=f_sm)

    img.save(os.path.join(OUT, filename))
    print(f"  [ok] {filename}")

# ── Generate all 54 cards ─────────────────────────────────────────────────────
#  Filename key → display label
VALUES = {
    "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
    "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
    "skip": "⊘", "reverse": "↺", "draw2": "+2",
}

print(f"Generating UNO card images -> {OUT}\n")
for color, (bg, dark) in PALETTE.items():
    for key, label in VALUES.items():
        make_color_card(f"{color}_{key}.png", bg, dark, label)

make_wild_card("wild.png", plus4=False)
make_wild_card("wild_draw4.png", plus4=True)

total = len(PALETTE) * len(VALUES) + 2
print(f"\nDone! {total} card images generated in:\n   {OUT}")

