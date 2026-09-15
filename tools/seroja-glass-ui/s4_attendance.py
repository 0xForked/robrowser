"""Section 4 — Check Attendance (488x413 calendar + 3 slot states + OK button).

Measured off the original: 20 day cells at x(27,89,151,213,275)+55,
y(96,160,224,288)+57; header band 0..85; right rail x338..470; footer y360+.
"""

import math
import os

import numpy as np

import glass as g
import icons as ic
from glass import (ACCENT, ACCENT2, BORDER, GOLD, MUTED, SUCCESS, TEXT, VIOLET,
                   Vec, add_light, blur_np, layer, mask_to_np, over, paste,
                   ring_mask, rr_mask, vgrad)

OUT = os.environ.get("OUT", "../p22/P22/new-assets") + "/check_attendance"

COLS = (27, 89, 151, 213, 275)
ROWS = (96, 160, 224, 288)
CELL = (56, 58)


def attendance_bg():
    w, h = 488, 413
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(24, 42, 78), tint_bot=(8, 14, 28),
        alpha_top=0.74, alpha_bot=0.63, border_alpha=0.50,
        ticks=True, inner_glow=0.26,
    )
    # header band — the old art had a paper banner here
    a = over(a, g.inset_well(w, h, (16, 14, w - 16, 76), radius=13, fill=(10, 18, 36),
                             fill_alpha=0.52, depth=0.32, glow=0.14))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    band = np.zeros((h, w), dtype=np.float32)
    band[14:76, 16:w - 16] = 1.0
    a = add_light(a, ACCENT, np.clip(1 - np.abs((xx - w * 0.5) / (w * 0.45)), 0, 1) ** 2 * band * 0.10)
    # header ornament: a small constellation of pips
    v = Vec(w, h)
    for i in range(7):
        x = 60 + i * 62
        v.ellipse([x - 1.6, 68, x + 1.6, 71.2], fill=255)
    a = over(a, layer(w, h, BORDER, v.mask() * 0.30))

    # 20 day-slot wells
    for ry in ROWS:
        for cx in COLS:
            a = over(a, g.inset_well(w, h, (cx, ry, cx + CELL[0], ry + CELL[1]), radius=g.RADIUS_SM,
                                     fill=(10, 18, 34), fill_alpha=0.52, depth=0.34,
                                     border_alpha=0.26, glow=0.05))
    # right rail: info bubble + reward tray
    a = over(a, g.inset_well(w, h, (340, 90, 470, 262), radius=13, fill=(11, 20, 38),
                             fill_alpha=0.50, depth=0.30, border_alpha=0.30, glow=0.08))
    a = over(a, g.inset_well(w, h, (340, 272, 470, 346), radius=13, fill=(12, 22, 42),
                             fill_alpha=0.55, depth=0.32, border_alpha=0.34, glow=0.14, glow_color=GOLD))
    # footer tray for the OK button
    a = over(a, g.divider(w, h, 360, 20, w - 20, alpha=0.22))
    pool = np.zeros((h, w), dtype=np.float32)
    pool[362:h - 10, 20:w - 20] = 1.0
    a = add_light(a, ACCENT, blur_np(pool, 12.0) * 0.05)
    return a


def bt_ok(press):
    return g.button(146, 30, radius=g.RADIUS_SM, tone="blue",
                    state="press" if press else "on", label="OK", font_size=14)


def bt_slot(state):
    """58x60 day slot: 'off' = future, 'a' = claimable today, 'complete' = claimed."""
    w, h = 58, 60
    if state == "a":
        tile = g.slot(w, h, radius=g.RADIUS_SM, state="on")
        # pulsing ring + a plus sign: "claim me"
        v = Vec(w, h)
        ic.plus(v, w / 2, h / 2 + 2, 22, w=3.4)
        m = v.mask()
        tile = add_light(tile, ACCENT, blur_np(m, 3.4) * 0.75)
        tile = over(tile, layer(w, h, (240, 250, 255), m * 0.96))
        halo = np.clip(mask_to_np(rr_mask(w, h, g.RADIUS_SM))
                       - mask_to_np(rr_mask(w, h, g.RADIUS_SM, inset=3.0)), 0, 1)
        tile = add_light(tile, ACCENT, blur_np(halo, 3.2) * 0.55)
    elif state == "complete":
        tile = g.slot(w, h, radius=g.RADIUS_SM, state="off")
        tile = add_light(tile, SUCCESS, mask_to_np(rr_mask(w, h, g.RADIUS_SM)) * 0.035)
        v = Vec(w, h)
        ic.check(v, w / 2, h / 2 + 1, 40, w=5.0)
        m = v.mask()
        tile = add_light(tile, SUCCESS, blur_np(m, 3.4) * 0.70)
        tile = over(tile, layer(w, h, (198, 255, 224), m * 0.95))
        tile = add_light(tile, SUCCESS, blur_np(ring_mask(w, h, g.RADIUS_SM, 1.3), 2.6) * 0.40)
    else:  # off / not reached yet
        tile = g.slot(w, h, radius=g.RADIUS_SM, state="lock")
        v = Vec(w, h)
        v.ellipse([w / 2 - 6, h / 2 - 6, w / 2 + 6, h / 2 + 6], outline=255, width=1.6)
        m = v.mask()
        tile = over(tile, layer(w, h, MUTED, m * 0.42))
    return tile


BUILD = {
    "attendance_bg.png": (attendance_bg, (488, 413)),
    "bt_ok_normal.png": (lambda: bt_ok(False), (146, 30)),
    "bt_ok_press.png": (lambda: bt_ok(True), (146, 30)),
    "bt_slot_a.png": (lambda: bt_slot("a"), (58, 60)),
    "bt_slot_off.png": (lambda: bt_slot("off"), (58, 60)),
    "bt_slot_complete.png": (lambda: bt_slot("complete"), (58, 60)),
}

if __name__ == "__main__":
    for name, (fn, size) in BUILD.items():
        arr = fn()
        got = (arr.shape[1], arr.shape[0])
        assert got == size, f"{name}: expected {size}, got {got}"
        g.save(arr, os.path.join(OUT, name))
    print(f"check_attendance: {len(BUILD)} files -> {OUT}")
