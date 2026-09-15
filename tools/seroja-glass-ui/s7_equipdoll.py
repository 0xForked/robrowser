"""Section 7 — Equipment doll silhouette backgrounds.

The gear slots are plain glass squares in CSS now, so these backgrounds stay
deliberately empty at the left and right thirds (that's where the slots land)
and only carry the centred character silhouette the reskin dropped.
"""

import math
import os

import numpy as np

import glass as g
from glass import (ACCENT, ACCENT2, BORDER, MUTED, TEXT, VIOLET, Vec,
                   add_light, blur_np, layer, mask_to_np, over, paste,
                   ring_mask, rr_mask, vgrad)

OUT = os.environ.get("OUT", "../p22/P22/new-assets") + "/equipment_doll"


def silhouette(v, cx, cy, s):
    """Stylised humanoid, unit height ~1.0*s, centred on cx,cy."""
    head_r = .092 * s
    v.ellipse([cx - head_r, cy - .50 * s, cx + head_r, cy - .50 * s + head_r * 2], fill=255)
    # neck
    v.rrect([cx - .030 * s, cy - .345 * s, cx + .030 * s, cy - .300 * s], .012 * s, fill=255)
    # torso
    v.poly([(cx - .150 * s, cy - .300 * s), (cx - .165 * s, cy - .250 * s),
            (cx - .098 * s, cy - .040 * s), (cx - .112 * s, cy + .055 * s),
            (cx + .112 * s, cy + .055 * s), (cx + .098 * s, cy - .040 * s),
            (cx + .165 * s, cy - .250 * s), (cx + .150 * s, cy - .300 * s)], fill=255)
    # arms
    for sgn in (-1, 1):
        v.poly([(cx + sgn * .150 * s, cy - .300 * s), (cx + sgn * .215 * s, cy - .275 * s),
                (cx + sgn * .205 * s, cy - .040 * s), (cx + sgn * .190 * s, cy + .095 * s),
                (cx + sgn * .140 * s, cy + .090 * s), (cx + sgn * .150 * s, cy - .045 * s)], fill=255)
        v.ellipse([cx + sgn * .205 * s - .030 * s, cy + .080 * s,
                   cx + sgn * .205 * s + .030 * s, cy + .140 * s], fill=255)
    # legs
    for sgn in (-1, 1):
        v.poly([(cx + sgn * .012 * s, cy + .045 * s), (cx + sgn * .098 * s, cy + .045 * s),
                (cx + sgn * .092 * s, cy + .270 * s), (cx + sgn * .080 * s, cy + .455 * s),
                (cx + sgn * .022 * s, cy + .455 * s), (cx + sgn * .030 * s, cy + .270 * s)], fill=255)
        fx0 = cx + sgn * .022 * s - (.022 * s if sgn < 0 else 0)
        fx1 = cx + sgn * .098 * s + (.022 * s if sgn > 0 else 0)
        v.rrect([min(fx0, fx1), cy + .440 * s, max(fx0, fx1), cy + .490 * s], .015 * s, fill=255)


def doll_bg(w, h, variant="general"):
    a = np.zeros((h, w, 4), dtype=np.float32)
    cx, cy = w * 0.5, h * 0.50
    s = h * 0.94

    # a soft column of light the figure stands in
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    col = np.clip(1.0 - np.abs(xx - cx) / (w * 0.16), 0, 1) ** 1.6
    col *= np.clip(np.sin(np.linspace(0, math.pi, h, dtype=np.float32)), 0, 1)[:, None] ** 0.7
    a = add_light(a, ACCENT if variant != "costume" else VIOLET, col * 0.10)

    v = Vec(w, h)
    silhouette(v, cx, cy, s)
    m = v.mask()
    accent = {"general": ACCENT, "costume": VIOLET, "switch": ACCENT2}.get(variant, ACCENT)

    # bloom, body, rim — a hologram rather than a solid figure
    a = over(a, layer(w, h, accent, blur_np(m, 6.0) * 0.30))
    a = over(a, layer(w, h, accent, blur_np(m, 2.2) * 0.26))
    fill = np.zeros((h, w, 4), dtype=np.float32)
    grad = vgrad(h, w, 0.44, 0.16, gamma=0.8)
    fill = over(fill, layer(w, h, (120, 180, 248) if variant != "costume" else (176, 150, 255), m * grad))
    a = over(a, fill)
    rim = np.clip(m - blur_np(m, 1.4), 0, 1)
    a = add_light(a, (210, 238, 255), rim * 0.55)

    # horizontal scan lines across the figure — holographic tell
    scan = ((np.arange(h) % 3) == 0).astype(np.float32)[:, None] * np.ones((1, w), dtype=np.float32)
    a[..., 3] *= 1.0 - scan * m * 0.16

    # ground pad
    pad = mask_to_np(g.ellipse_mask(w, h, [cx - w * .13, h - 12, cx + w * .13, h - 3]))
    a = add_light(a, accent, blur_np(pad, 3.0) * 0.30)

    # faint centre rail so the empty sides read as intentional
    a = over(a, g.divider(w, h, h - 6, int(w * 0.30), int(w * 0.70), alpha=0.16))
    return a


BUILD = {
    "equipwin_bg.png": (lambda: doll_bg(280, 130, "general"), (280, 130)),
    "equipwin_special.png": (lambda: doll_bg(280, 133, "costume"), (280, 133)),
    "equipwin_bg2.png": (lambda: doll_bg(280, 157, "general"), (280, 157)),
    "equipwin_bg2_change.png": (lambda: doll_bg(280, 179, "switch"), (280, 179)),
    "equipwin_special_change.png": (lambda: doll_bg(280, 179, "costume"), (280, 179)),
}

if __name__ == "__main__":
    for name, (fn, size) in BUILD.items():
        arr = fn()
        got = (arr.shape[1], arr.shape[0])
        assert got == size, f"{name}: expected {size}, got {got}"
        g.save(arr, os.path.join(OUT, name))
    print(f"equipment_doll: {len(BUILD)} files -> {OUT}")
