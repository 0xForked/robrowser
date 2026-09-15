"""Section 8 — Storage category tabs.

Each 20x209 file is a full vertical tab column (7 cells of ~29.8px), and the
seven files differ by which cell is selected — that's how the originals are
built. Same idea for the 20x82 set (3 cells). Every cell now carries a real
category icon instead of the old rotated micro-text.
"""

import os

import numpy as np

import glass as g
import icons as ic
from glass import (ACCENT, BORDER, MUTED, TEXT, Vec, add_light, blur_np, layer,
                   mask_to_np, over, paste, ring_mask, rr_mask)

OUT = os.environ.get("OUT", "../p22/P22/new-assets") + "/storage_tabs"

CATS_7 = [
    ("consumable", ic.potion), ("equipment", ic.armor), ("card", ic.card),
    ("weapon", ic.sword), ("ammo", ic.arrow_ammo), ("misc", ic.box), ("favorite", ic.star),
]
CATS_3 = [("consumable", ic.potion), ("equipment", ic.armor), ("misc", ic.box)]


def tab_cell(w, h, draw_icon, on):
    if on:
        tile = g.glass_panel(
            w, h, radius=7, corners=(True, False, False, True),
            tint_top=(36, 76, 130), tint_bot=(18, 40, 76),
            alpha_top=0.96, alpha_bot=0.92, border_alpha=0.70,
            ticks=False, inner_glow=0.42, vignette=0.14, noise=0.0,
        )
        tile = add_light(tile, ACCENT, blur_np(ring_mask(w, h, 7, 1.3, corners=(1, 0, 0, 1)), 2.6) * 0.60)
        rail = np.zeros((h, w), dtype=np.float32)
        rail[3:h - 3, 1:3] = 1.0
        tile = add_light(tile, ACCENT, blur_np(rail, 1.8) * 0.9)
    else:
        tile = g.glass_panel(
            w, h, radius=7, corners=(True, False, False, True),
            tint_top=(17, 28, 50), tint_bot=(9, 15, 29),
            alpha_top=0.80, alpha_bot=0.74, border_alpha=0.24,
            ticks=False, inner_glow=0.08, vignette=0.24, noise=0.0,
        )
    v = Vec(w, h)
    draw_icon(v, w * 0.54, h * 0.5, min(w * 0.72, h * 0.50))
    m = v.mask()
    if on:
        tile = add_light(tile, ACCENT, blur_np(m, 2.2) * 0.65)
        tile = over(tile, layer(w, h, (238, 249, 255), m * 0.97))
    else:
        tile = over(tile, layer(w, h, (2, 6, 14), blur_np(m, 1.0) * 0.30))
        tile = over(tile, layer(w, h, MUTED, m * 0.78))
    return tile


def tab_column(w, h, cats, selected):
    out = np.zeros((h, w, 4), dtype=np.float32)
    n = len(cats)
    edges = [round(i * h / n) for i in range(n + 1)]
    for i, (_, icon) in enumerate(cats):
        y0, y1 = edges[i], edges[i + 1]
        out = paste(out, tab_cell(w, y1 - y0, icon, i == selected), 0, y0)
    return out


BUILD = {}
for _i in range(7):
    BUILD[f"tab_itm_ex_0{_i + 1}.png"] = (lambda i=_i: tab_column(20, 209, CATS_7, i), (20, 209))
for _i in range(3):
    BUILD[f"tab_itm_0{_i + 1}.png"] = (lambda i=_i: tab_column(20, 82, CATS_3, i), (20, 82))

if __name__ == "__main__":
    for name, (fn, size) in BUILD.items():
        arr = fn()
        got = (arr.shape[1], arr.shape[0])
        assert got == size, f"{name}: expected {size}, got {got}"
        g.save(arr, os.path.join(OUT, name))
    print(f"storage_tabs: {len(BUILD)} files -> {OUT}")
