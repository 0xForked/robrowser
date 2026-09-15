"""Section 2 — Cash Shop (723x540 + cart, tabs, buttons, arrows).

Structural boxes were measured off the original bitmaps so everything the
client pixel-positions on top still lands where it used to:
  promo banner   x1..536   y16..71
  item grid      3x3 cells x(11,186,361)+166  y(108,235,363)+121
  right rail     x536..723
  cart rows      6 rows    x5..173  y5..340 step 57
"""

import math
import os

import numpy as np

import glass as g
from glass import (ACCENT, ACCENT2, BORDER, GOLD, MUTED, SUCCESS, TEXT, VIOLET,
                   Vec, add_light, blur_np, layer, mask_to_np, over, paste,
                   ring_mask, rr_mask, vgrad)

OUT = os.environ.get("OUT", "../p22/P22/new-assets") + "/cashshop"


def img_shop_bg():
    w, h = 723, 540
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(22, 38, 70), tint_bot=(8, 14, 28),
        alpha_top=0.72, alpha_bot=0.62, border_alpha=0.50,
        ticks=True, inner_glow=0.24,
    )
    # promo banner — deeper well with an accent wash, like a lit billboard
    a = over(a, g.inset_well(w, h, (10, 18, 530, 70), radius=12, fill=(6, 11, 24),
                             fill_alpha=0.66, depth=0.40, glow=0.18))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    band = np.zeros((h, w), dtype=np.float32)
    band[18:70, 10:530] = 1.0
    wash = np.clip(1.0 - np.abs((xx - 170) / 300.0), 0, 1) ** 2 * band
    a = add_light(a, ACCENT, wash * 0.10)
    a = add_light(a, VIOLET, np.clip(1.0 - np.abs((xx - 430) / 260.0), 0, 1) ** 2 * band * 0.07)

    # filter / sort strip
    a = over(a, g.inset_well(w, h, (10, 78, 530, 102), radius=8, fill=(8, 14, 28),
                             fill_alpha=0.40, depth=0.26, border_alpha=0.20))

    # 3x3 item cards
    for cy_ in (108, 235, 363):
        for cx_ in (11, 186, 361):
            a = over(a, g.inset_well(w, h, (cx_, cy_, cx_ + 166, cy_ + 121), radius=12,
                                     fill=(12, 21, 40), fill_alpha=0.50, depth=0.30,
                                     border_alpha=0.30, glow=0.07))

    # vertical rail separating the cart column
    rail = np.zeros((h, w), dtype=np.float32)
    rail[18:h - 18, 534] = 1.0
    fade = np.clip(np.sin(np.linspace(0, math.pi, h, dtype=np.float32)) * 1.5, 0, 1)[:, None]
    a = over(a, layer(w, h, BORDER, rail * fade * 0.30))
    a = add_light(a, ACCENT, blur_np(rail * fade, 3.0) * 0.28)

    # currency strip at the top of the rail
    a = over(a, g.inset_well(w, h, (546, 24, 712, 56), radius=9, fill=(10, 18, 34),
                             fill_alpha=0.55, depth=0.30, glow=0.12, glow_color=GOLD))
    # bottom search bar tray
    a = over(a, g.inset_well(w, h, (12, 508, 528, 532), radius=10, fill=(8, 14, 28),
                             fill_alpha=0.52, depth=0.34, border_alpha=0.26))
    a = over(a, g.divider(w, h, 498, 10, 530, alpha=0.18))
    return a


def img_shop_cart_bg():
    w, h = 185, 350
    a = g.glass_panel(
        w, h, radius=12,
        tint_top=(24, 42, 76), tint_bot=(9, 16, 32),
        alpha_top=0.68, alpha_bot=0.58, border_alpha=0.46,
        ticks=False, inner_glow=0.26,
    )
    for y0 in (5, 62, 119, 176, 233, 290):
        a = over(a, g.inset_well(w, h, (5, y0, 172, y0 + 49), radius=9, fill=(11, 19, 36),
                                 fill_alpha=0.55, depth=0.30, border_alpha=0.28))
    # scrollbar gutter
    a = over(a, g.inset_well(w, h, (175, 4, 182, h - 4), radius=3, fill=(6, 11, 22),
                             fill_alpha=0.55, depth=0.22, border_alpha=0.16))
    return a


# 9 category tabs, 56x31 — one hue step each so the row reads as a spectrum
TAB_TONES = [
    (79, 195, 247), (56, 189, 248), (99, 179, 255), (129, 166, 255),
    (167, 139, 250), (216, 130, 230), (255, 140, 170), (255, 170, 110), (120, 220, 190),
]


def shop_tab(idx, on):
    w, h = 56, 31
    accent = TAB_TONES[idx]
    if on:
        tile = g.glass_panel(
            w, h, radius=9, corners=(True, True, False, False),
            tint_top=(34, 72, 124), tint_bot=(18, 40, 76),
            alpha_top=0.96, alpha_bot=0.92, border_alpha=0.70,
            ticks=False, inner_glow=0.40, vignette=0.14,
        )
        tile = add_light(tile, accent, blur_np(ring_mask(w, h, 9, 1.4, corners=(1, 1, 0, 0)), 2.8) * 0.55)
        under = np.zeros((h, w), dtype=np.float32)
        under[h - 2:h, 4:w - 4] = 1.0
        tile = add_light(tile, accent, blur_np(under, 2.0) * 0.85)
        tile = over(tile, layer(w, h, accent, under * 0.85))
    else:
        tile = g.glass_panel(
            w, h, radius=9, corners=(True, True, False, False),
            tint_top=(18, 29, 52), tint_bot=(10, 16, 30),
            alpha_top=0.80, alpha_bot=0.74, border_alpha=0.28,
            ticks=False, inner_glow=0.10, vignette=0.24,
        )
        tile = add_light(tile, accent, mask_to_np(rr_mask(w, h, 9, corners=(1, 1, 0, 0))) * 0.018)
    # tiny type-marker pip so tabs are distinguishable even unlabelled
    v = Vec(w, h)
    v.ellipse([w / 2 - 2.2, 7, w / 2 + 2.2, 11.4], fill=255)
    m = v.mask()
    tile = add_light(tile, accent, blur_np(m, 2.2) * (0.9 if on else 0.45))
    tile = over(tile, layer(w, h, (235, 248, 255) if on else MUTED, m * (0.95 if on else 0.55)))
    return tile


def btn_buy_normal():
    return g.button(154, 23, radius=8, tone="blue", state="on", label="BUY", font_size=12)


def btn_charge_normal():
    return g.button(64, 20, radius=7, tone="gold", state="normal", label="CHARGE", font_size=9)


def btn_searchbar_normal():
    w, h = 54, 18
    a = g.glass_panel(
        w, h, radius=7, tint_top=(26, 48, 86), tint_bot=(13, 24, 46),
        alpha_top=0.92, alpha_bot=0.86, border_alpha=0.50, ticks=False,
        inner_glow=0.22, vignette=0.18,
    )
    v = Vec(w, h)
    cx, cy, r = w * 0.5 - 1.5, h * 0.5 - 0.5, 4.2
    v.ellipse([cx - r, cy - r, cx + r, cy + r], outline=255, width=1.6)
    v.line([(cx + r * 0.72, cy + r * 0.72), (cx + r * 1.7, cy + r * 1.7)], width=1.8)
    m = v.mask()
    a = add_light(a, ACCENT, blur_np(m, 2.0) * 0.5)
    a = over(a, layer(w, h, (225, 243, 255), m * 0.95))
    return a


def arrow(w, h, direction, on, double=False):
    tile = g.glass_panel(
        w, h, radius=4,
        tint_top=(32, 62, 108) if on else (16, 26, 46),
        tint_bot=(15, 30, 58) if on else (9, 14, 27),
        alpha_top=0.92 if on else 0.78, alpha_bot=0.86 if on else 0.72,
        border_alpha=0.60 if on else 0.28, ticks=False,
        inner_glow=0.30 if on else 0.10, vignette=0.14, noise=0.0,
    )
    v = Vec(w, h)
    cy = h / 2.0
    sx = 1 if direction == "R" else -1
    tips = [w / 2 + sx * 1.6] if not double else [w / 2 - sx * 1.6, w / 2 + sx * 4.2]
    for tx in tips:
        v.poly([(tx, cy - 3.2), (tx + sx * 3.2, cy), (tx, cy + 3.2)], fill=255)
    m = v.mask()
    col = (235, 248, 255) if on else MUTED
    if on:
        tile = add_light(tile, ACCENT, blur_np(m, 2.0) * 0.6)
    tile = over(tile, layer(w, h, col, m * (0.98 if on else 0.62)))
    return tile


BUILD = {
    "img_shop_bg.png": (img_shop_bg, (723, 540)),
    "img_shop_cart_bg.png": (img_shop_cart_bg, (185, 350)),
    "btn_buy_normal.png": (btn_buy_normal, (154, 23)),
    "btn_charge_normal.png": (btn_charge_normal, (64, 20)),
    "btn_searchbar_normal.png": (btn_searchbar_normal, (54, 18)),
    "bt_arrowL_off.png": (lambda: arrow(11, 12, "L", False), (11, 12)),
    "bt_arrowL_on.png": (lambda: arrow(11, 12, "L", True), (11, 12)),
    "bt_arrowR_off.png": (lambda: arrow(11, 12, "R", False), (11, 12)),
    "bt_arrowR_on.png": (lambda: arrow(11, 12, "R", True), (11, 12)),
    "bt_arrowL2_off.png": (lambda: arrow(16, 12, "L", False, True), (16, 12)),
    "bt_arrowL2_on.png": (lambda: arrow(16, 12, "L", True, True), (16, 12)),
    "bt_arrowR2_off.png": (lambda: arrow(16, 12, "R", False, True), (16, 12)),
    "bt_arrowR2_on.png": (lambda: arrow(16, 12, "R", True, True), (16, 12)),
}
for _i in range(9):
    BUILD[f"img_shop_tap{_i}_off.png"] = (lambda i=_i: shop_tab(i, False), (56, 31))
    BUILD[f"img_shop_tap{_i}_on.png"] = (lambda i=_i: shop_tab(i, True), (56, 31))

if __name__ == "__main__":
    for name, (fn, size) in BUILD.items():
        arr = fn()
        got = (arr.shape[1], arr.shape[0])
        assert got == size, f"{name}: expected {size}, got {got}"
        g.save(arr, os.path.join(OUT, name))
    print(f"cashshop: {len(BUILD)} files -> {OUT}")
