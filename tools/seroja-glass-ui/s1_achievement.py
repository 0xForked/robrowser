"""Section 1 — Achievement window (750x466, a dozen stitched pieces)."""

import math
import os

import numpy as np

import glass as g
from glass import (ACCENT, ACCENT2, BORDER, GOLD, MUTED, SUCCESS, TEXT, VIOLET,
                   Vec, add_light, blur_np, layer, mask_to_np, over, paste,
                   ring_mask, rr_mask, vgrad)

OUT = os.environ.get("OUT", "../p22/P22/new-assets") + "/achievement"


def metal(w, h, m, stops, spec=0.55, spec_y=0.28):
    """Fill a coverage mask with a vertical metal ramp + a specular band."""
    t = np.linspace(0, 1, h, dtype=np.float32)
    cols = np.zeros((h, 3), dtype=np.float32)
    ps = [p for p, _ in stops]
    for i in range(3):
        cols[:, i] = np.interp(t, ps, [c[i] / 255.0 for _, c in stops])
    rgb = np.broadcast_to(cols[:, None, :], (h, w, 3)).copy()
    out = np.concatenate([rgb, m[..., None]], axis=-1)
    band = np.clip(1.0 - np.abs(t - spec_y) * 9.0, 0, 1)[:, None] ** 1.5
    out = add_light(out, (255, 255, 255), band * m * spec)
    return out


def emboss(tile, m, up=(255, 255, 255), down=(0, 0, 0), amt=0.35):
    """Cheap bevel: brighten where the mask rises, darken where it falls."""
    top = np.clip(m - np.roll(m, 1, axis=0), 0, 1)
    bot = np.clip(m - np.roll(m, -1, axis=0), 0, 1)
    tile = add_light(tile, up, blur_np(top, 0.7) * amt)
    h, w = m.shape
    tile = over(tile, layer(w, h, down, blur_np(bot, 0.7) * amt * 0.8))
    return tile


# ---------------------------------------------------------------- 750x46 ---
def bg_upper():
    w, h = 750, 46
    a = g.titlebar(w, h, radius=g.RADIUS)
    # left accent pip where the trophy icon sits
    v = Vec(w, h)
    v.rrect([14, 13, 18, h - 13], 2, fill=255)
    m = v.mask()
    a = add_light(a, ACCENT, blur_np(m, 3.0) * 0.75)
    a = over(a, layer(w, h, (200, 235, 255), m * 0.9))
    # faint tick marks along the strip — HUD texture, no implied layout
    v2 = Vec(w, h)
    for x in range(230, w - 120, 22):
        v2.line([(x, h - 7), (x, h - 4)], width=1.0)
    a = over(a, layer(w, h, BORDER, v2.mask() * 0.13))
    return a


# --------------------------------------------------------------- 102x405 ---
def bg_tab():
    w, h = 102, 405
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(24, 42, 76), tint_bot=(9, 16, 32),
        alpha_top=0.66, alpha_bot=0.56, border_alpha=0.50,
        ticks=True, inner_glow=0.30,
    )
    # vertical accent rail down the inner edge
    rail = np.zeros((h, w), dtype=np.float32)
    rail[10:h - 10, w - 4] = 1.0
    fade = np.clip(np.sin(np.linspace(0, math.pi, h, dtype=np.float32)) * 1.6, 0, 1)[:, None]
    a = add_light(a, ACCENT, blur_np(rail * fade, 2.4) * 0.40)
    return a


# --------------------------------------------------------------- 309x405 ---
def bg_list():
    w, h = 309, 405
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(22, 38, 70), tint_bot=(9, 15, 30),
        alpha_top=0.64, alpha_bot=0.55, border_alpha=0.48,
        ticks=True, inner_glow=0.28,
    )
    a = over(a, g.divider(w, h, 34, 16, w - 16, alpha=0.20))
    return a


# --------------------------------------------------------------- 648x404 ---
def bg_summary():
    w, h = 648, 404
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(23, 40, 73), tint_bot=(9, 15, 30),
        alpha_top=0.64, alpha_bot=0.55, border_alpha=0.48,
        ticks=True, inner_glow=0.26,
    )
    # very faint trophy watermark, centred — texture only, nothing to align to
    v = Vec(w, h)
    cx, cy, s = w * 0.5, h * 0.52, 3.1
    _trophy_path(v, cx, cy, s * 22, outline_only=True)
    wm = v.mask()
    a = add_light(a, (120, 175, 245), blur_np(wm, 2.0) * 0.055)
    a = over(a, g.divider(w, h, 40, 20, w - 20, alpha=0.18))
    return a


# --------------------------------------------------------------- 328x405 ---
def bg_detail():
    w, h = 328, 405
    a = g.glass_panel(
        w, h, radius=g.RADIUS,
        tint_top=(26, 45, 82), tint_bot=(9, 16, 32),
        alpha_top=0.68, alpha_bot=0.57, border_alpha=0.52,
        ticks=True, inner_glow=0.32,
    )
    a = over(a, g.divider(w, h, 44, 18, w - 18, alpha=0.22))
    # soft accent pool behind where the reward row sits, bottom third
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w * 0.5) / (w * 0.7)) ** 2 + ((yy - h * 0.80) / (h * 0.30)) ** 2)
    pool = np.clip(1.0 - d, 0, 1) ** 2.4
    a = add_light(a, ACCENT, pool * mask_to_np(rr_mask(w, h, g.RADIUS)) * 0.09)
    return a


# ----------------------------------------------------------------- 64x54 ---
def detail_stamp():
    """A translucent 'CLEAR' ink stamp, tilted like it was pressed by hand."""
    S = 4
    W, H = 64 * S, 54 * S
    big = 64 * S * 2
    v = g.Vec(128, 108)  # 2x working canvas, rotated then downscaled
    cx, cy, r = 64, 54, 44
    v.ellipse([cx - r, cy - r, cx + r, cy + r], outline=255, width=5.0)
    v.ellipse([cx - r + 9, cy - r + 9, cx + r - 9, cy + r - 9], outline=255, width=2.0)
    # check mark
    v.line([(cx - 20, cy + 1), (cx - 6, cy + 15), (cx + 22, cy - 18)], width=8.0)
    # serrations
    for i in range(24):
        a0 = i * 15.0
        rad = math.radians(a0)
        x0 = cx + math.cos(rad) * (r + 3)
        y0 = cy + math.sin(rad) * (r + 3)
        x1 = cx + math.cos(rad) * (r + 7)
        y1 = cy + math.sin(rad) * (r + 7)
        v.line([(x0, y0), (x1, y1)], width=2.0)
    m = v.mask()
    im = g.Image.fromarray(np.clip(m * 255, 0, 255).astype(np.uint8), "L")
    im = im.rotate(-13, resample=g.Image.BICUBIC, expand=False)
    im = im.resize((64, 54), g.Image.LANCZOS)
    m = mask_to_np(im)

    w, h = 64, 54
    out = np.zeros((h, w, 4), dtype=np.float32)
    out = over(out, layer(w, h, SUCCESS, blur_np(m, 3.2) * 0.55))
    out = over(out, layer(w, h, ACCENT, blur_np(m, 1.4) * 0.35))
    out = over(out, layer(w, h, (196, 255, 224), m * 0.92))
    return out


# ----------------------------------------------------------------- 39x40 ---
def _trophy_path(v, cx, cy, s, outline_only=False):
    """Trophy silhouette centred on cx,cy; s = half-width of the bowl."""
    w = s
    top = cy - s * 1.05
    bowl = [
        (cx - w, top), (cx + w, top),
        (cx + w * 0.92, cy - s * 0.15), (cx + w * 0.55, cy + s * 0.35),
        (cx, cy + s * 0.50), (cx - w * 0.55, cy + s * 0.35),
        (cx - w * 0.92, cy - s * 0.15),
    ]
    if outline_only:
        v.poly(bowl, fill=0, outline=255, width=max(1.0, s * 0.10))
    else:
        v.poly(bowl, fill=255)
    # handles
    hw = max(1.6, s * 0.30)
    v.arc([cx - w * 1.70, top - s * 0.02, cx - w * 0.40, cy - s * 0.02], -70, 118, width=hw)
    v.arc([cx + w * 0.40, top - s * 0.02, cx + w * 1.70, cy - s * 0.02], 62, 250, width=hw)
    # stem + base
    if outline_only:
        v.rect([cx - s * 0.16, cy + s * 0.44, cx + s * 0.16, cy + s * 0.86], outline=255, width=max(1.0, s * 0.09))
        v.rrect([cx - s * 0.62, cy + s * 0.84, cx + s * 0.62, cy + s * 1.12], s * 0.10,
                outline=255, width=max(1.0, s * 0.09))
    else:
        v.poly([(cx - s * 0.17, cy + s * 0.42), (cx + s * 0.17, cy + s * 0.42),
                (cx + s * 0.24, cy + s * 0.86), (cx - s * 0.24, cy + s * 0.86)], fill=255)
        v.rrect([cx - s * 0.64, cy + s * 0.84, cx + s * 0.64, cy + s * 1.14], s * 0.10, fill=255)


def upper_trophy():
    w, h = 39, 40
    v = Vec(w, h)
    _trophy_path(v, w * 0.5, h * 0.47, 10.4)
    m = v.mask()
    tile = metal(w, h, m, [
        (0.00, (255, 236, 176)), (0.28, (255, 205, 96)),
        (0.62, (214, 150, 44)), (1.00, (146, 96, 24)),
    ], spec=0.45, spec_y=0.22)
    tile = emboss(tile, m, amt=0.28)
    # engraved star on the bowl
    v2 = Vec(w, h)
    v2.star(w * 0.5, h * 0.40, 4.6, 1.9)
    sm = v2.mask() * m
    tile = over(tile, layer(w, h, (120, 70, 16), sm * 0.55))
    tile = add_light(tile, (255, 250, 220), blur_np(sm, 0.8) * 0.25)
    # cyan rim light so it belongs to the glass UI
    rim = np.clip(m - blur_np(m, 1.3), 0, 1)
    tile = add_light(tile, ACCENT, rim * 0.30)
    out = np.zeros((h, w, 4), dtype=np.float32)
    out = over(out, layer(w, h, GOLD, blur_np(m, 3.0) * 0.40))
    out = over(out, layer(w, h, ACCENT, blur_np(m, 5.0) * 0.16))
    return over(out, tile)


# ----------------------------------------------------------------- 12x12 ---
def btn_radio(on):
    w, h = 12, 12
    out = np.zeros((h, w, 4), dtype=np.float32)
    disc = mask_to_np(g.ellipse_mask(w, h, [0.6, 0.6, w - 0.6, h - 0.6]))
    ring = np.clip(disc - mask_to_np(g.ellipse_mask(w, h, [0.6, 0.6, w - 0.6, h - 0.6], inset=1.3)), 0, 1)
    if on:
        out = over(out, layer(w, h, ACCENT, blur_np(disc, 2.4) * 0.55))
        out = over(out, layer(w, h, (12, 26, 48), disc * 0.92))
        out = over(out, layer(w, h, (176, 224, 255), ring * 0.95))
        dot = mask_to_np(g.ellipse_mask(w, h, [3.3, 3.3, w - 3.3, h - 3.3]))
        out = add_light(out, ACCENT, blur_np(dot, 1.6) * 0.85)
        out = over(out, layer(w, h, (225, 245, 255), dot * 0.98))
    else:
        out = over(out, layer(w, h, (10, 17, 32), disc * 0.80))
        out = over(out, layer(w, h, MUTED, ring * 0.58))
        gl = np.clip(disc - mask_to_np(g.ellipse_mask(w, h, [0.6, 0.6, w - 0.6, h - 0.6], inset=1.3)), 0, 1)
        out = add_light(out, (120, 160, 210), gl * vgrad(h, w, 0.35, 0.0) * 0.5)
    return out


# ----------------------------------------------------------------- 62x62 ---
def reward_frame(kind):
    w, h = 62, 62
    # one shared blue-glass frame; the reward type only tints the rim + glyph
    accent = {"item": ACCENT, "buff": GOLD, "title": VIOLET}[kind]
    top, bot = (28, 50, 90), (11, 19, 36)
    tile = g.glass_panel(
        w, h, radius=g.RADIUS_SM,
        tint_top=top, tint_bot=bot,
        alpha_top=0.90, alpha_bot=0.84, border_alpha=0.55,
        ticks=False, inner_glow=0.34, vignette=0.22,
    )
    tile = add_light(tile, accent, blur_np(ring_mask(w, h, g.RADIUS_SM, 1.4), 3.0) * 0.45)
    # soft light pool behind the glyph
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w * 0.45)) ** 2 + ((yy - h * 0.52) / (h * 0.45)) ** 2)
    tile = add_light(tile, accent, np.clip(1 - d, 0, 1) ** 2 * mask_to_np(rr_mask(w, h, g.RADIUS_SM)) * 0.16)

    v = Vec(w, h)
    if kind == "item":
        # faceted crystal
        cx, cy = w * 0.5, h * 0.52
        v.poly([(cx, cy - 19), (cx + 13, cy - 4), (cx, cy + 19), (cx - 13, cy - 4)], fill=255)
        m = v.mask()
        tile = over(tile, layer(w, h, (150, 220, 255), blur_np(m, 3.0) * 0.55))
        body = metal(w, h, m, [(0.0, (222, 246, 255)), (0.35, (120, 200, 250)),
                               (0.75, (46, 130, 210)), (1.0, (22, 70, 140))], spec=0.30, spec_y=0.25)
        tile = over(tile, body)
        f = Vec(w, h)
        f.line([(cx, cy - 19), (cx, cy + 19)], width=1.0)
        f.line([(cx - 13, cy - 4), (cx + 13, cy - 4)], width=1.0)
        f.line([(cx - 13, cy - 4), (cx, cy - 19), (cx + 13, cy - 4)], width=1.0)
        fm = f.mask() * m
        tile = add_light(tile, (235, 252, 255), fm * 0.55)
    elif kind == "buff":
        # upward chevrons over a rounded badge => "boost"
        cx, cy = w * 0.5, h * 0.53
        v.rrect([cx - 17, cy - 17, cx + 17, cy + 17], 9, fill=110)
        for i, off in enumerate((7, -2, -11)):
            a = 255 - i * 45
            v.line([(cx - 10, cy + off + 5), (cx, cy + off - 4), (cx + 10, cy + off + 5)], width=3.2, fill=a)
        m = v.mask()
        tile = over(tile, layer(w, h, (255, 220, 150), blur_np(m, 3.0) * 0.45))
        tile = over(tile, metal(w, h, m, [(0.0, (255, 246, 214)), (0.4, (255, 208, 118)),
                                          (1.0, (214, 142, 40))], spec=0.35, spec_y=0.20))
    else:
        # title = unfurled scroll
        cx, cy = w * 0.5, h * 0.52
        v.rrect([cx - 15, cy - 13, cx + 15, cy + 13], 4, fill=255)
        m_body = v.mask()
        tile = over(tile, layer(w, h, (210, 190, 255), blur_np(m_body, 3.0) * 0.45))
        tile = over(tile, metal(w, h, m_body, [(0.0, (250, 244, 232)), (0.45, (226, 214, 236)),
                                               (1.0, (150, 134, 186))], spec=0.30, spec_y=0.22))
        r = Vec(w, h)
        r.rrect([cx - 20, cy - 16, cx - 12, cy + 16], 4, fill=255)
        r.rrect([cx + 12, cy - 16, cx + 20, cy + 16], 4, fill=255)
        rm = r.mask()
        tile = over(tile, metal(w, h, rm, [(0.0, (196, 170, 255)), (0.5, (140, 112, 220)),
                                           (1.0, (78, 58, 140))], spec=0.40, spec_y=0.25))
        t = Vec(w, h)
        for i, yy_ in enumerate((-7, -1, 5)):
            t.line([(cx - 9 + (i == 2) * 3, cy + yy_), (cx + 9 - (i == 1) * 4, cy + yy_)], width=1.2)
        tile = over(tile, layer(w, h, (92, 74, 140), t.mask() * m_body * 0.85))
        m = np.clip(m_body + rm, 0, 1)

    glowm = m if kind != "title" else np.clip(m_body + rm, 0, 1)
    tile = add_light(tile, accent, blur_np(glowm, 5.0) * 0.14)
    return tile


BUILD = {
    "bg_upper.png": (bg_upper, (750, 46)),
    "bg_tab.png": (bg_tab, (102, 405)),
    "bg_list.png": (bg_list, (309, 405)),
    "bg_summary.png": (bg_summary, (648, 404)),
    "bg_detail.png": (bg_detail, (328, 405)),
    "detail_stamp.png": (detail_stamp, (64, 54)),
    "upper_trophy.png": (upper_trophy, (39, 40)),
    "btn_radio_off.png": (lambda: btn_radio(False), (12, 12)),
    "btn_radio_on.png": (lambda: btn_radio(True), (12, 12)),
    "reward_item.png": (lambda: reward_frame("item"), (62, 62)),
    "reward_buff.png": (lambda: reward_frame("buff"), (62, 62)),
    "reward_title.png": (lambda: reward_frame("title"), (62, 62)),
}

if __name__ == "__main__":
    for name, (fn, size) in BUILD.items():
        arr = fn()
        got = (arr.shape[1], arr.shape[0])
        assert got == size, f"{name}: expected {size}, got {got}"
        g.save(arr, os.path.join(OUT, name))
        print(f"  {name:22s} {got[0]}x{got[1]}")
    print(f"achievement: {len(BUILD)} files -> {OUT}")
