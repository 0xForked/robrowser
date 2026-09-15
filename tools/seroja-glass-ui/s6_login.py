"""Section 6 — Login card (301x132).

Real <input>/<button> elements sit invisibly on top at fixed offsets, so the
drawn field frames must land exactly where the originals were:
  server dropdown x14..171 y11..30   (arrow well x151..171)
  username       x14..171 y38..56
  password       x14..171 y62..80
  remember box   x58..67  y85..94
  Login button   circle centred (238,72) r45
  close X        circle centred (283,22) r11
"""

import math
import os

import numpy as np

import glass as g
import icons as ic
from glass import (ACCENT, ACCENT2, BORDER, GOLD, MUTED, SUCCESS, TEXT, VIOLET,
                   Vec, add_light, blur_np, layer, mask_to_np, over, paste,
                   ring_mask, rr_mask, vgrad)

OUT = os.environ.get("OUT", "../p22/P22/new-assets") + "/win_login"


def bg_login():
    w, h = 301, 132
    a = g.glass_panel(
        w, h, radius=14,
        tint_top=(26, 46, 84), tint_bot=(8, 14, 28),
        alpha_top=0.86, alpha_bot=0.76, border_alpha=0.55,
        ticks=True, inner_glow=0.32,
    )
    # field frames
    for (x0, y0, x1, y1) in ((14, 11, 171, 30), (14, 38, 171, 56), (14, 62, 171, 80)):
        a = over(a, g.inset_well(w, h, (x0, y0, x1, y1), radius=7, fill=(7, 12, 25),
                                 fill_alpha=0.62, depth=0.36, border_alpha=0.34, glow=0.08))
    # dropdown chevron well on the server row
    a = over(a, g.inset_well(w, h, (151, 12, 170, 29), radius=6, fill=(16, 30, 56),
                             fill_alpha=0.70, depth=0.20, border_alpha=0.30))
    v = Vec(w, h)
    v.poly([(157, 18.5), (164.5, 18.5), (160.75, 23.5)], fill=255)
    m = v.mask()
    a = add_light(a, ACCENT, blur_np(m, 1.8) * 0.5)
    a = over(a, layer(w, h, (220, 240, 255), m * 0.9))

    # remember-me checkbox frame
    a = over(a, g.inset_well(w, h, (58, 85, 68, 95), radius=3, fill=(7, 12, 25),
                             fill_alpha=0.66, depth=0.28, border_alpha=0.40))
    # small caption rule under the fields
    a = over(a, g.divider(w, h, 104, 14, 172, alpha=0.16))

    # ---- the round Login button -------------------------------------------
    bcx, bcy, br = 238.0, 72.0, 45.0
    disc = mask_to_np(g.ellipse_mask(w, h, [bcx - br, bcy - br, bcx + br, bcy + br]))
    a = over(a, layer(w, h, ACCENT, blur_np(disc, 9.0) * 0.30))
    ramp = vgrad(h, w, 1.0, 0.0, 0.9)
    body = np.zeros((h, w, 4), dtype=np.float32)
    body = over(body, layer(w, h, (40, 96, 168), disc * 0.96))
    body = add_light(body, (70, 150, 230), disc * ramp * 0.42)
    body = add_light(body, ACCENT, disc * (1 - ramp) * 0.16)
    a = over(a, body)
    ring = np.clip(disc - mask_to_np(g.ellipse_mask(w, h, [bcx - br, bcy - br, bcx + br, bcy + br], inset=1.6)), 0, 1)
    a = add_light(a, ACCENT, blur_np(ring, 3.2) * 0.75)
    a = over(a, layer(w, h, (196, 230, 255), ring * 0.85))
    inner = np.clip(mask_to_np(g.ellipse_mask(w, h, [bcx - br + 6, bcy - br + 6, bcx + br - 6, bcy + br - 6]))
                    - mask_to_np(g.ellipse_mask(w, h, [bcx - br + 7.2, bcy - br + 7.2,
                                                       bcx + br - 7.2, bcy + br - 7.2])), 0, 1)
    a = over(a, layer(w, h, BORDER, inner * 0.35))
    # gloss cap
    gl = mask_to_np(g.ellipse_mask(w, h, [bcx - br * .78, bcy - br * .92, bcx + br * .78, bcy - br * .08]))
    a = add_light(a, (200, 232, 255), blur_np(gl, 5.0) * 0.20)
    a = over(a, g.text_np(w, h, (bcx, bcy + 1), "LOGIN", g.font("ui_b", 21),
                          color=(240, 250, 255), glow=ACCENT, glow_amount=0.45, shadow=0.55))

    # ---- close X -----------------------------------------------------------
    ccx, ccy, cr = 283.0, 22.0, 10.5
    cd = mask_to_np(g.ellipse_mask(w, h, [ccx - cr, ccy - cr, ccx + cr, ccy + cr]))
    a = over(a, layer(w, h, (16, 26, 46), cd * 0.88))
    cring = np.clip(cd - mask_to_np(g.ellipse_mask(w, h, [ccx - cr, ccy - cr, ccx + cr, ccy + cr], inset=1.3)), 0, 1)
    a = add_light(a, ACCENT, blur_np(cring, 2.4) * 0.45)
    a = over(a, layer(w, h, BORDER, cring * 0.70))
    v2 = Vec(w, h)
    ic.cross(v2, ccx, ccy, 13, w=1.8)
    xm = v2.mask()
    a = over(a, layer(w, h, (226, 242, 255), xm * 0.92))

    # SeROja wordmark in the dead space above the fields' left margin
    a = over(a, g.text_np(w, h, (16, 112), "SeROja", g.font("display", 17),
                          color=(196, 226, 255), anchor="lm", glow=ACCENT, glow_amount=0.30, shadow=0.5))
    a = over(a, g.text_np(w, h, (86, 114), "ONLINE", g.font("tech", 9),
                          color=MUTED, anchor="lm", glow=None, shadow=0.4))
    return a


BUILD = {"bg_login.png": (bg_login, (301, 132))}

if __name__ == "__main__":
    for name, (fn, size) in BUILD.items():
        arr = fn()
        got = (arr.shape[1], arr.shape[0])
        assert got == size, f"{name}: expected {size}, got {got}"
        g.save(arr, os.path.join(OUT, name))
    print(f"win_login: {len(BUILD)} files -> {OUT}")
