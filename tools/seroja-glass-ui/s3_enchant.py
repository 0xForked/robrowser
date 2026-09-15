"""Section 3 — Enchant Grade (400x330).

The original is not literally a wheel: it's an enchant machine illustration in
the left column (x0..140, keyed out with magenta) plus a UI panel on the right
(x140..400). That zone split is kept so the client's hardcoded offsets still
land, but the machine is redrawn as a glowing rune array in the glass language.
"""

import math
import os

import numpy as np

import glass as g
import icons as ic
from glass import (ACCENT, ACCENT2, BORDER, GOLD, MUTED, SUCCESS, TEXT, VIOLET,
                   Vec, add_light, blur_np, layer, mask_to_np, over, paste,
                   ring_mask, rr_mask, vgrad)

OUT = os.environ.get("OUT", "../p22/P22/new-assets") + "/enchant_grade"


def rune_array(w, h, cx, cy, r):
    """Concentric rune circle with ticks and a hot core — the enchant altar."""
    out = np.zeros((h, w, 4), dtype=np.float32)
    v = Vec(w, h)
    v.ellipse([cx - r, cy - r, cx + r, cy + r], outline=255, width=1.4)
    v.ellipse([cx - r * .80, cy - r * .80, cx + r * .80, cy + r * .80], outline=255, width=1.0)
    v.ellipse([cx - r * .46, cy - r * .46, cx + r * .46, cy + r * .46], outline=255, width=1.2)
    for i in range(36):
        a = math.radians(i * 10)
        long_ = (i % 3 == 0)
        r0 = r * (0.84 if long_ else 0.88)
        r1 = r * 0.97
        v.line([(cx + math.cos(a) * r0, cy + math.sin(a) * r0),
                (cx + math.cos(a) * r1, cy + math.sin(a) * r1)], width=1.0)
    # inscribed hexagram
    for rot in (-90, -30):
        pts = [(cx + math.cos(math.radians(rot + k * 120)) * r * .70,
                cy + math.sin(math.radians(rot + k * 120)) * r * .70) for k in range(3)]
        v.poly(pts + [pts[0]], fill=0, outline=255, width=1.2)
    m = v.mask()
    out = over(out, layer(w, h, ACCENT, blur_np(m, 4.0) * 0.45))
    out = over(out, layer(w, h, (190, 232, 255), m * 0.80))

    # hot core
    core = mask_to_np(g.ellipse_mask(w, h, [cx - r * .24, cy - r * .24, cx + r * .24, cy + r * .24]))
    out = over(out, layer(w, h, ACCENT, blur_np(core, r * 0.30) * 0.60))
    out = over(out, layer(w, h, (235, 250, 255), core * 0.88))
    return out


def bg_grade_enchant():
    w, h = 400, 330
    a = np.zeros((h, w, 4), dtype=np.float32)

    # right-hand UI panel (the part the original had opaque)
    panel = g.glass_panel(
        260, h - 8, radius=g.RADIUS,
        tint_top=(24, 42, 78), tint_bot=(8, 14, 28),
        alpha_top=0.74, alpha_bot=0.63, border_alpha=0.50,
        ticks=True, inner_glow=0.26,
    )
    a = paste(a, panel, 140, 4)
    a = over(a, g.inset_well(w, h, (152, 30, 388, 92), radius=11, fill=(8, 14, 28),
                             fill_alpha=0.58, depth=0.36, glow=0.14))
    a = over(a, g.inset_well(w, h, (152, 100, 388, 212), radius=11, fill=(10, 18, 34),
                             fill_alpha=0.46, depth=0.30, border_alpha=0.26))
    for y0 in (222, 258):
        a = over(a, g.inset_well(w, h, (166, y0, 388, y0 + 30), radius=9, fill=(11, 19, 36),
                                 fill_alpha=0.52, depth=0.28, border_alpha=0.28))
    a = over(a, g.inset_well(w, h, (166, 296, 388, 320), radius=8, fill=(8, 14, 28),
                             fill_alpha=0.50, depth=0.30, glow=0.10, glow_color=GOLD))

    # left column: the altar, floating on transparency like the original
    col = g.glass_panel(
        128, 300, radius=g.RADIUS,
        tint_top=(20, 36, 70), tint_bot=(7, 12, 26),
        alpha_top=0.50, alpha_bot=0.40, border_alpha=0.38,
        ticks=True, inner_glow=0.30, vignette=0.34,
    )
    a = paste(a, col, 6, 16)
    a = over(a, rune_array(w, h, 70, 150, 50))
    # beam rising from the array into the socket above
    beam = np.zeros((h, w), dtype=np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    beam = np.clip(1 - np.abs(xx - 70) / 26.0, 0, 1) * np.clip((150 - yy) / 90.0, 0, 1)
    a = add_light(a, ACCENT, beam * 0.16)
    # the socket / receiver plate
    a = over(a, g.inset_well(w, h, (40, 40, 100, 66), radius=9, fill=(10, 18, 34),
                             fill_alpha=0.66, depth=0.34, glow=0.24))
    # material tray below the array
    a = over(a, g.inset_well(w, h, (26, 236, 114, 296), radius=10, fill=(10, 18, 34),
                             fill_alpha=0.52, depth=0.32, border_alpha=0.30))
    return a


def btn_start():
    return g.button(82, 28, radius=9, tone="blue", state="on", label="START", font_size=13)


def btn_unbroken(state):
    """28x40 vertical secondary button — hover ('over') and pressed ('pick')."""
    w, h = 28, 40
    tile = g.button(w, h, radius=9, tone="blue", state="on" if state == "over" else "press")
    v = Vec(w, h)
    ic.sparkle(v, w / 2, h / 2, 20)
    m = v.mask()
    col = (240, 250, 255) if state == "over" else (200, 228, 255)
    tile = add_light(tile, ACCENT, blur_np(m, 3.0) * (0.75 if state == "over" else 0.45))
    tile = over(tile, layer(w, h, col, m * 0.95))
    return tile


BUILD = {
    "bg_grade_enchant.png": (bg_grade_enchant, (400, 330)),
    "btn_start.png": (btn_start, (82, 28)),
    "btn_unbroken_over.png": (lambda: btn_unbroken("over"), (28, 40)),
    "btn_unbroken_pick.png": (lambda: btn_unbroken("pick"), (28, 40)),
}

if __name__ == "__main__":
    for name, (fn, size) in BUILD.items():
        arr = fn()
        got = (arr.shape[1], arr.shape[0])
        assert got == size, f"{name}: expected {size}, got {got}"
        g.save(arr, os.path.join(OUT, name))
    print(f"enchant_grade: {len(BUILD)} files -> {OUT}")
