"""Section 5 — Quest log.

bg_quest1..4 are NOT size variants (ASSETS.md is wrong about that): diffing the
originals shows they are identical except for the left tab column x0..30, where
variant N highlights tab N. Rebuilt on that reading.
Tab bands measured at y 18-115 / 119-216 / 220-317 / 321-418.
"""

import math
import os

import numpy as np
from PIL import Image

import glass as g
import icons as ic
from glass import (ACCENT, ACCENT2, BORDER, GOLD, MUTED, SUCCESS, TEXT, VIOLET,
                   Vec, add_light, blur_np, layer, mask_to_np, over, paste,
                   ring_mask, rr_mask, vgrad)

OUT = os.environ.get("OUT", "../p22/P22/new-assets") + "/quest"

TAB_BANDS = [(18, 115), (119, 216), (220, 317), (321, 418)]
TAB_LABELS = ["ACTIVE", "NEW QUESTS", "PENDING", "COOLDOWN"]
TAB_W = 30


def _vlabel(text, px, size=11, color=TEXT):
    """Bottom-to-top rotated label, returned as a float RGBA strip."""
    f = g.font("tech", size * g.SS)
    tmp = Image.new("L", (px * g.SS, 40 * g.SS), 0)
    d = g.ImageDraw.Draw(tmp)
    d.text((px * g.SS / 2, 20 * g.SS), text, font=f, fill=255, anchor="mm")
    tmp = tmp.rotate(90, expand=True)
    tmp = tmp.resize((40, px), Image.LANCZOS)
    return mask_to_np(tmp)


def quest_tabs(w, h, active):
    """Left category rail drawn onto a w*h canvas."""
    out = np.zeros((h, w, 4), dtype=np.float32)
    for i, (y0, y1) in enumerate(TAB_BANDS):
        th = y1 - y0
        on = (i == active)
        tile = g.glass_panel(
            TAB_W, th, radius=g.RADIUS_SM, corners=(True, False, False, True),
            tint_top=(34, 72, 124) if on else (16, 27, 48),
            tint_bot=(18, 40, 76) if on else (9, 15, 28),
            alpha_top=0.95 if on else 0.78, alpha_bot=0.90 if on else 0.72,
            border_alpha=0.66 if on else 0.26,
            ticks=False, inner_glow=0.38 if on else 0.10, vignette=0.20, noise=0.0,
        )
        if on:
            tile = add_light(tile, ACCENT, blur_np(ring_mask(TAB_W, th, g.RADIUS_SM, 1.4,
                                                             corners=(1, 0, 0, 1)), 3.0) * 0.55)
            rail = np.zeros((th, TAB_W), dtype=np.float32)
            rail[6:th - 6, 1:3] = 1.0
            tile = add_light(tile, ACCENT, blur_np(rail, 2.2) * 0.9)
        lab = _vlabel(TAB_LABELS[i], th, size=10)
        lm = np.zeros((th, TAB_W), dtype=np.float32)
        lw = min(40, TAB_W)
        lm[:, (TAB_W - lw) // 2:(TAB_W - lw) // 2 + lw] = lab[:, (40 - lw) // 2:(40 - lw) // 2 + lw]
        tile = over(tile, layer(TAB_W, th, (3, 7, 16), blur_np(lm, 1.1) * 0.5))
        tile = over(tile, layer(TAB_W, th, TEXT if on else MUTED, lm * (0.98 if on else 0.68)))
        if on:
            tile = add_light(tile, ACCENT, blur_np(lm, 2.4) * 0.22)
        out = paste(out, tile, 0, y0)
    return out


def bg_quest(active):
    w, h = 381, 466
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(22, 38, 70), tint_bot=(8, 14, 28),
        alpha_top=0.72, alpha_bot=0.62, border_alpha=0.50,
        ticks=True, inner_glow=0.26,
    )
    # content well to the right of the tab rail
    a = over(a, g.inset_well(w, h, (34, 22, w - 10, 424), radius=12, fill=(10, 18, 34),
                             fill_alpha=0.44, depth=0.30, border_alpha=0.26))
    a = over(a, g.divider(w, h, 432, 14, w - 14, alpha=0.20))
    a = over(a, quest_tabs(w, h, active))
    return a


def bg_questsub():
    w, h = 342, 412
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(24, 42, 76), tint_bot=(8, 14, 28),
        alpha_top=0.72, alpha_bot=0.62, border_alpha=0.50,
        ticks=True, inner_glow=0.26,
    )
    a = over(a, g.inset_well(w, h, (12, 20, w - 12, 58), radius=10, fill=(10, 18, 36),
                             fill_alpha=0.50, depth=0.28, glow=0.10))
    a = over(a, g.inset_well(w, h, (12, 66, w - 12, 382), radius=12, fill=(9, 16, 32),
                             fill_alpha=0.44, depth=0.30, border_alpha=0.24))
    # faint quest-scroll watermark where the poring used to be
    v = Vec(w, h)
    ic.scroll_icon(v, w * 0.5, h * 0.52, 190)
    a = add_light(a, (110, 165, 235), blur_np(v.mask(), 3.0) * 0.045)
    return a


def bg_questlist():
    w, h = 330, 46
    a = g.titlebar(w, h, radius=12)
    v = Vec(w, h)
    ic.flag(v, 20, h / 2, 20)
    m = v.mask()
    a = add_light(a, ACCENT, blur_np(m, 2.6) * 0.55)
    a = over(a, layer(w, h, (225, 243, 255), m * 0.92))
    return a


def quest_window():
    w, h = 350, 375
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(24, 42, 76), tint_bot=(8, 14, 28),
        alpha_top=0.74, alpha_bot=0.63, border_alpha=0.50,
        ticks=True, inner_glow=0.26,
    )
    a = over(a, g.divider(w, h, 40, 14, w - 14, alpha=0.22))
    a = over(a, g.inset_well(w, h, (12, 48, w - 12, 330), radius=12, fill=(9, 16, 32),
                             fill_alpha=0.46, depth=0.30, border_alpha=0.26))
    a = over(a, g.divider(w, h, 340, 14, w - 14, alpha=0.18))
    return a


def img_poring():
    """10x9 'new quest' marker — a bright accent pip with a soft halo."""
    w, h = 10, 9
    out = np.zeros((h, w, 4), dtype=np.float32)
    core = mask_to_np(g.ellipse_mask(w, h, [2.0, 1.5, w - 2.0, h - 1.5]))
    out = over(out, layer(w, h, ACCENT, blur_np(core, 2.2) * 0.70))
    out = over(out, layer(w, h, (190, 232, 255), core * 0.92))
    hi = mask_to_np(g.ellipse_mask(w, h, [3.2, 2.2, 6.4, 4.6]))
    out = add_light(out, (255, 255, 255), hi * 0.55)
    return out


def img_questiocn():
    """38x38 quest marker icon (the original filename's typo is preserved)."""
    w, h = 38, 38
    tile = g.glass_panel(
        w, h, radius=g.RADIUS_SM, tint_top=(30, 56, 100), tint_bot=(12, 22, 42),
        alpha_top=0.92, alpha_bot=0.86, border_alpha=0.58, ticks=False,
        inner_glow=0.34, vignette=0.20,
    )
    tile = add_light(tile, GOLD, blur_np(ring_mask(w, h, g.RADIUS_SM, 1.3), 2.8) * 0.35)
    v = Vec(w, h)
    # exclamation mark — the universal RO quest marker
    v.rrect([w / 2 - 2.6, 8, w / 2 + 2.6, 23], 2.2, fill=255)
    v.ellipse([w / 2 - 2.8, 25.5, w / 2 + 2.8, 31.1], fill=255)
    m = v.mask()
    tile = add_light(tile, GOLD, blur_np(m, 3.0) * 0.75)
    tile = over(tile, layer(w, h, (255, 243, 212), m * 0.96))
    return tile


BUILD = {
    "bg_quest1.png": (lambda: bg_quest(0), (381, 466)),
    "bg_quest2.png": (lambda: bg_quest(1), (381, 466)),
    "bg_quest3.png": (lambda: bg_quest(2), (381, 466)),
    "bg_quest4.png": (lambda: bg_quest(3), (381, 466)),
    "bg_questsub.png": (bg_questsub, (342, 412)),
    "bg_questlist.png": (bg_questlist, (330, 46)),
    "quest_window.png": (quest_window, (350, 375)),
    "img_poring.png": (img_poring, (10, 9)),
    "img_questiocn.png": (img_questiocn, (38, 38)),
}

if __name__ == "__main__":
    for name, (fn, size) in BUILD.items():
        arr = fn()
        got = (arr.shape[1], arr.shape[0])
        assert got == size, f"{name}: expected {size}, got {got}"
        g.save(arr, os.path.join(OUT, name))
    print(f"quest: {len(BUILD)} files -> {OUT}")
