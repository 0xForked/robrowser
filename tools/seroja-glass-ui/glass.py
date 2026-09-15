"""SeROja Glass UI — drawing primitives.

Everything is rendered at SS x supersample and box/LANCZOS-downsampled so the
1px hairlines and 16px corner radii stay crisp at the exact target canvas size.

Palette tokens mirror robrowser/src/UI/Components/SeROjaCommon/glassTheme.css.
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SS = 4  # supersample factor

# ---------------------------------------------------------------- palette ---
BG = (6, 10, 20)  # --sj-bg          #060a14
GLASS = (18, 30, 54)  # --sj-glass       rgba(18,30,54,.55)
GLASS_SOLID = (16, 26, 46)  # --sj-glass-solid #101a2e
BORDER = (148, 197, 255)  # --sj-border      rgba(148,197,255,.22)
TEXT = (234, 242, 255)  # --sj-text        #eaf2ff
MUTED = (143, 163, 196)  # --sj-muted       #8fa3c4
ACCENT = (79, 195, 247)  # --sj-accent      #4fc3f7
ACCENT2 = (56, 189, 248)  # --sj-accent-2    #38bdf8
DANGER = (255, 92, 92)  # --sj-danger      #ff5c5c
SUCCESS = (74, 222, 128)  # --sj-success     #4ade80
GOLD = (255, 201, 92)  # warm accent for trophies / currency
VIOLET = (167, 139, 250)  # rare/title accent

RADIUS = 16  # --sj-radius
RADIUS_SM = 10  # --sj-radius-sm

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
_FONTS = {
    "ui": "Outfit-Regular.ttf",
    "ui_b": "Outfit-Bold.ttf",
    "tech": "Jura-Medium.ttf",
    "tech_l": "Jura-Light.ttf",
    "display": "BigShoulders-Bold.ttf",
    "serif": "Gloock-Regular.ttf",
    "mono": "GeistMono-Bold.ttf",
}


def font(name, size):
    path = os.path.join(FONT_DIR, _FONTS.get(name, name))
    if not os.path.exists(path):
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)


# ------------------------------------------------------------- numpy glue ---
def to_np(img):
    """RGBA PIL -> float32 array (h,w,4) in 0..1."""
    return np.asarray(img.convert("RGBA"), dtype=np.float32) / 255.0


def to_img(arr):
    return Image.fromarray(np.clip(arr * 255.0 + 0.5, 0, 255).astype(np.uint8), "RGBA")


def mask_to_np(m):
    return np.asarray(m, dtype=np.float32) / 255.0


def blank(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def over(dst, src):
    """Alpha-composite src over dst; both float arrays (h,w,4)."""
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    oa = sa + da * (1.0 - sa)
    safe = np.where(oa > 1e-6, oa, 1.0)
    rgb = (src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)) / safe
    out = np.concatenate([rgb, oa], axis=-1)
    return np.where(oa > 1e-6, out, 0.0)


def layer(w, h, rgb, alpha_mask):
    """Build a float RGBA layer of a flat colour modulated by a float mask."""
    a = np.asarray(alpha_mask, dtype=np.float32)
    if a.ndim == 2:
        a = a[..., None]
    c = np.asarray(rgb, dtype=np.float32) / 255.0
    return np.concatenate([np.broadcast_to(c, (h, w, 3)).copy(), a], axis=-1)


def add_light(base, rgb, alpha_mask, amount=1.0):
    """Screen-ish additive light — keeps glass looking emissive, not painted."""
    a = np.asarray(alpha_mask, dtype=np.float32)
    if a.ndim == 2:
        a = a[..., None]
    c = np.asarray(rgb, dtype=np.float32) / 255.0
    out = base.copy()
    out[..., :3] = np.clip(base[..., :3] + c * a * amount, 0, 1)
    out[..., 3:4] = np.clip(base[..., 3:4] + a * amount * 0.85, 0, 1)
    return out


# ------------------------------------------------------------------ masks ---
def rr_mask(w, h, r, inset=0.0, corners=(True, True, True, True)):
    """Anti-aliased rounded-rectangle coverage mask at 1:1 size."""
    im = Image.new("L", (int(w * SS), int(h * SS)), 0)
    d = ImageDraw.Draw(im)
    i = inset * SS
    rad = max(0.0, (r - inset)) * SS
    box = [i, i, w * SS - i, h * SS - i]
    if box[2] <= box[0] or box[3] <= box[1]:
        return im.resize((w, h), Image.LANCZOS)
    if rad <= 0.5:
        d.rectangle(box, fill=255)
    else:
        d.rounded_rectangle(box, radius=rad, fill=255, corners=corners)
    return im.resize((w, h), Image.LANCZOS)


def ring_mask(w, h, r, width=1.0, inset=0.0, corners=(True, True, True, True)):
    """Hairline stroke following a rounded rect."""
    outer = mask_to_np(rr_mask(w, h, r, inset, corners))
    inner = mask_to_np(rr_mask(w, h, r, inset + width, corners))
    return np.clip(outer - inner, 0, 1)


def ellipse_mask(w, h, box, inset=0.0):
    im = Image.new("L", (int(w * SS), int(h * SS)), 0)
    d = ImageDraw.Draw(im)
    b = [(box[0] + inset) * SS, (box[1] + inset) * SS, (box[2] - inset) * SS, (box[3] - inset) * SS]
    d.ellipse(b, fill=255)
    return im.resize((w, h), Image.LANCZOS)


def blur_np(mask, radius):
    """Gaussian-blur a float mask via PIL."""
    m = Image.fromarray(np.clip(mask * 255, 0, 255).astype(np.uint8), "L")
    m = m.filter(ImageFilter.GaussianBlur(radius))
    return mask_to_np(m)


def vgrad(h, w, top, bot, gamma=1.0):
    """Vertical 0..1 ramp broadcast to (h,w)."""
    t = np.linspace(0.0, 1.0, h, dtype=np.float32) ** gamma
    return (top + (bot - top) * t)[:, None] * np.ones((1, w), dtype=np.float32)


def hgrad(h, w, left, right, gamma=1.0):
    t = np.linspace(0.0, 1.0, w, dtype=np.float32) ** gamma
    return np.ones((h, 1), dtype=np.float32) * (left + (right - left) * t)[None, :]


# ------------------------------------------------- vector drawing helpers ---
class Vec:
    """Supersampled vector scratch layer; .mask() returns a float coverage map."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.im = Image.new("L", (int(w * SS), int(h * SS)), 0)
        self.d = ImageDraw.Draw(self.im)

    def s(self, v):
        if isinstance(v, (list, tuple)):
            return [x * SS for x in v]
        return v * SS

    def line(self, pts, width=1.0, fill=255, joint="curve"):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=fill, width=max(1, int(width * SS)), joint=joint)

    def poly(self, pts, fill=255, outline=None, width=1.0):
        p = [(x * SS, y * SS) for x, y in pts]
        self.d.polygon(p, fill=fill, outline=outline, width=max(1, int(width * SS)) if outline else 0)

    def ellipse(self, box, fill=None, outline=None, width=1.0):
        self.d.ellipse(self.s(box), fill=fill, outline=outline, width=max(1, int(width * SS)) if outline else 0)

    def rrect(self, box, r, fill=None, outline=None, width=1.0, corners=(True, True, True, True)):
        self.d.rounded_rectangle(
            self.s(box), radius=r * SS, fill=fill, outline=outline,
            width=max(1, int(width * SS)) if outline else 0, corners=corners,
        )

    def rect(self, box, fill=None, outline=None, width=1.0):
        self.d.rectangle(self.s(box), fill=fill, outline=outline, width=max(1, int(width * SS)) if outline else 0)

    def arc(self, box, start, end, width=1.0, fill=255):
        self.d.arc(self.s(box), start, end, fill=fill, width=max(1, int(width * SS)))

    def pieslice(self, box, start, end, fill=255):
        self.d.pieslice(self.s(box), start, end, fill=fill)

    def text(self, xy, txt, fnt, fill=255, anchor="mm", spacing=0):
        f = ImageFont.truetype(fnt.path, int(fnt.size * SS)) if hasattr(fnt, "path") else fnt
        self.d.text((xy[0] * SS, xy[1] * SS), txt, font=f, fill=fill, anchor=anchor)

    def star(self, cx, cy, r_out, r_in, points=5, rot=-90, fill=255):
        pts = []
        for i in range(points * 2):
            a = math.radians(rot + i * 180.0 / points)
            r = r_out if i % 2 == 0 else r_in
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        self.poly(pts, fill=fill)

    def ngon(self, cx, cy, r, n, rot=-90, fill=255, outline=None, width=1.0):
        pts = []
        for i in range(n):
            a = math.radians(rot + i * 360.0 / n)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        self.poly(pts, fill=fill, outline=outline, width=width)

    def mask(self):
        return mask_to_np(self.im.resize((self.w, self.h), Image.LANCZOS))


def glyph(w, h, draw_fn, color=TEXT, glow=ACCENT, glow_radius=2.2, glow_amount=0.55):
    """Render a vector glyph with a soft coloured bloom behind it."""
    v = Vec(w, h)
    draw_fn(v)
    m = v.mask()
    out = np.zeros((h, w, 4), dtype=np.float32)
    if glow is not None and glow_amount > 0:
        g = blur_np(m, glow_radius)
        out = over(out, layer(w, h, glow, np.clip(g * glow_amount, 0, 1)))
    out = over(out, layer(w, h, color, m))
    return out, m


# ------------------------------------------------------------ glass panel ---
def glass_panel(
    w,
    h,
    radius=RADIUS,
    corners=(True, True, True, True),
    tint_top=(26, 44, 78),
    tint_bot=(10, 18, 34),
    alpha_top=0.62,
    alpha_bot=0.50,
    border_alpha=0.52,
    border_width=1.0,
    rim=True,
    ticks=True,
    sheen=True,
    inner_glow=0.30,
    vignette=0.28,
    noise=0.010,
):
    """The base frosted-glass surface every window/panel is built from."""
    m = mask_to_np(rr_mask(w, h, radius, corners=corners))

    # body: vertical tint ramp
    t = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
    ct = np.asarray(tint_top, dtype=np.float32) / 255.0
    cb = np.asarray(tint_bot, dtype=np.float32) / 255.0
    rgb = ct[None, None, :] + (cb - ct)[None, None, :] * t
    rgb = np.broadcast_to(rgb, (h, w, 3)).copy()

    alpha = vgrad(h, w, alpha_top, alpha_bot, gamma=0.85) * m
    base = np.concatenate([rgb, alpha[..., None]], axis=-1)

    # soft radial sheen from the upper-left, like light through frosted glass
    if sheen:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        cx, cy = w * 0.26, h * 0.10
        rad = max(w, h) * 0.95
        d = np.sqrt(((xx - cx) / rad) ** 2 + ((yy - cy) / rad) ** 2)
        s = np.clip(1.0 - d, 0, 1) ** 2.1
        base = add_light(base, (120, 178, 255), s * m * 0.085)

        # thin diagonal light streak
        streak = np.clip(1.0 - np.abs((xx * 0.55 + yy) / (h + w * 0.55) - 0.30) * 7.0, 0, 1) ** 2
        base = add_light(base, (150, 200, 255), streak * m * 0.030)

    # vignette to keep the middle readable and the edges deep
    if vignette:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        nx = (xx / max(w - 1, 1)) * 2 - 1
        ny = (yy / max(h - 1, 1)) * 2 - 1
        vg = np.clip((nx ** 2 * 0.55 + ny ** 2 * 0.75), 0, 1) ** 1.4
        base[..., :3] *= 1.0 - vg[..., None] * vignette
        base[..., 3] = np.clip(base[..., 3] + vg * m * 0.10, 0, 1)

    # inner glow hugging the border (the "rim light" instead of a hard outline)
    if inner_glow:
        edge = np.clip(m - mask_to_np(rr_mask(w, h, radius, inset=max(2.0, radius * 0.22), corners=corners)), 0, 1)
        edge = blur_np(edge, max(1.2, radius * 0.18))
        base = add_light(base, ACCENT, edge * m * inner_glow)
        base = add_light(base, (120, 180, 255), blur_np(edge, 5.0) * m * inner_glow * 0.5)

    # rim light: bloom first, then the hairline itself on top
    if rim:
        hl = ring_mask(w, h, radius, width=border_width, inset=0.0, corners=corners)
        fade = vgrad(h, w, 1.0, 0.46, gamma=0.7)
        # outward-and-inward bloom so the border reads as light, not ink
        base = add_light(base, ACCENT, blur_np(hl, 3.0) * fade * border_alpha * 1.15)
        base = add_light(base, ACCENT2, blur_np(hl, 1.3) * fade * border_alpha * 0.85)
        base = over(base, layer(w, h, (176, 216, 255), hl * fade * border_alpha * 1.25))
        # brighter crown along the very top edge
        topfade = np.clip(1.0 - np.linspace(0, 1, h, dtype=np.float32) * 6.0, 0, 1)[:, None]
        base = add_light(base, (214, 238, 255), hl * topfade * 0.42)
        # faint inner second line for glass thickness
        inner = ring_mask(w, h, radius, width=1.0, inset=border_width + 1.0, corners=corners)
        base = over(base, layer(w, h, (10, 18, 36), inner * 0.26))

    # HUD corner ticks
    if ticks:
        base = over(base, corner_ticks(w, h, radius, corners=corners))

    # a whisper of grain so large flats don't band
    if noise:
        rng = np.random.default_rng(7)
        n = rng.normal(0, 1, (h, w)).astype(np.float32)
        n = blur_np(np.clip(n * 0.5 + 0.5, 0, 1), 0.6) - 0.5
        base[..., :3] = np.clip(base[..., :3] + n[..., None] * noise, 0, 1)

    return base


def corner_ticks(w, h, radius, corners=(True, True, True, True), length=None, inset=None, alpha=0.55, color=ACCENT):
    """Small L-brackets in the panel corners — the sci-fi HUD tell."""
    length = length if length is not None else max(6.0, min(w, h) * 0.055)
    length = min(length, min(w, h) * 0.30)
    inset = inset if inset is not None else max(3.0, radius * 0.42)
    v = Vec(w, h)
    lw = 1.0
    o = inset
    r = max(2.0, radius * 0.45)
    spec = [
        (corners[0], [(o, o + length + r), (o, o + r), (o + r, o), (o + length + r, o)]),
        (corners[1], [(w - o, o + length + r), (w - o, o + r), (w - o - r, o), (w - o - length - r, o)]),
        (corners[2], [(w - o, h - o - length - r), (w - o, h - o - r), (w - o - r, h - o), (w - o - length - r, h - o)]),
        (corners[3], [(o, h - o - length - r), (o, h - o - r), (o + r, h - o), (o + length + r, h - o)]),
    ]
    for on, pts in spec:
        if on:
            v.line(pts, width=lw, fill=255)
    m = v.mask()
    out = np.zeros((h, w, 4), dtype=np.float32)
    out = over(out, layer(w, h, color, blur_np(m, 1.4) * alpha * 0.5))
    out = over(out, layer(w, h, (190, 228, 255), m * alpha))
    return out


def inset_well(
    w,
    h,
    box,
    radius=RADIUS_SM,
    depth=0.30,
    border_alpha=0.26,
    fill=(8, 14, 28),
    fill_alpha=0.42,
    glow=0.0,
    glow_color=ACCENT,
):
    """A recessed area (list body, grid, input) drawn onto a w*h canvas."""
    x0, y0, x1, y1 = box
    bw, bh = int(round(x1 - x0)), int(round(y1 - y0))
    if bw <= 0 or bh <= 0:
        return np.zeros((h, w, 4), dtype=np.float32)
    m = mask_to_np(rr_mask(bw, bh, radius))
    tile = np.zeros((bh, bw, 4), dtype=np.float32)
    tile = over(tile, layer(bw, bh, fill, m * fill_alpha))
    # top-inner shadow => recessed
    sh = np.clip(m - mask_to_np(rr_mask(bw, bh, radius, inset=2.4)), 0, 1)
    sh = blur_np(sh, 1.8) * vgrad(bh, bw, 1.0, 0.25)
    tile = over(tile, layer(bw, bh, (4, 8, 18), sh * depth))
    # hairline
    tile = over(tile, layer(bw, bh, BORDER, ring_mask(bw, bh, radius, 1.0) * border_alpha))
    # bottom light catch
    tile = add_light(tile, (140, 190, 255), ring_mask(bw, bh, radius, 1.0) * vgrad(bh, bw, 0.0, 1.0, 3.0) * 0.20)
    if glow:
        g = blur_np(ring_mask(bw, bh, radius, 1.2), 2.6)
        tile = add_light(tile, glow_color, g * glow)
    out = np.zeros((h, w, 4), dtype=np.float32)
    return paste(out, tile, int(round(x0)), int(round(y0)))


def paste(dst, tile, x, y):
    """Alpha-composite `tile` (float RGBA) onto `dst` at x,y with clipping."""
    H, W = dst.shape[:2]
    th, tw = tile.shape[:2]
    sx0, sy0 = max(0, -x), max(0, -y)
    dx0, dy0 = max(0, x), max(0, y)
    dx1, dy1 = min(W, x + tw), min(H, y + th)
    if dx1 <= dx0 or dy1 <= dy0:
        return dst
    sub = tile[sy0:sy0 + (dy1 - dy0), sx0:sx0 + (dx1 - dx0)]
    dst[dy0:dy1, dx0:dx1] = over(dst[dy0:dy1, dx0:dx1], sub)
    return dst


def button(
    w,
    h,
    radius=RADIUS_SM,
    state="normal",
    tone="blue",
    ticks=False,
    label=None,
    font_name="ui_b",
    font_size=None,
    label_color=None,
):
    """Standalone glass button tile (float RGBA)."""
    tones = {
        "blue": ((36, 78, 132), (16, 34, 64), ACCENT),
        "ghost": ((22, 36, 62), (12, 20, 38), BORDER),
        "green": ((26, 86, 62), (12, 34, 28), SUCCESS),
        "red": ((104, 36, 44), (40, 14, 20), DANGER),
        "gold": ((104, 76, 26), (40, 28, 10), GOLD),
        "violet": ((70, 48, 118), (26, 18, 48), VIOLET),
    }
    top, bot, accent = tones.get(tone, tones["blue"])
    if state == "on":
        top = tuple(min(255, int(c * 1.45 + 14)) for c in top)
        bot = tuple(min(255, int(c * 1.35 + 8)) for c in bot)
    elif state == "press":
        top, bot = bot, top
    elif state == "off":
        top = tuple(int(c * 0.70) for c in top)
        bot = tuple(int(c * 0.70) for c in bot)

    tile = glass_panel(
        w, h, radius=radius,
        tint_top=top, tint_bot=bot,
        alpha_top=0.94 if state != "off" else 0.80,
        alpha_bot=0.88 if state != "off" else 0.74,
        border_alpha=0.70 if state in ("on", "press") else 0.46,
        ticks=ticks, inner_glow=0.30 if state == "on" else 0.16,
        vignette=0.18, noise=0.008,
    )
    if state == "on":
        edge = blur_np(ring_mask(w, h, radius, 1.4), 2.4)
        tile = add_light(tile, accent, edge * 0.55)
        tile = add_light(tile, accent, mask_to_np(rr_mask(w, h, radius)) * 0.05)
    # glossy top third
    m = mask_to_np(rr_mask(w, h, radius, inset=1.2))
    gloss = np.clip(1.0 - np.linspace(0, 1, h, dtype=np.float32) * 2.6, 0, 1)[:, None] ** 1.6
    tile = add_light(tile, (170, 212, 255), gloss * m * (0.16 if state != "press" else 0.05))

    if label:
        fs = font_size or max(8, int(h * 0.46))
        f = font(font_name, fs)
        v = Vec(w, h)
        v.text((w / 2.0, h / 2.0 - h * 0.03), label, f, fill=255, anchor="mm")
        lm = v.mask()
        tile = over(tile, layer(w, h, (2, 6, 14), blur_np(lm, 1.1) * 0.45))
        tile = over(tile, layer(w, h, label_color or TEXT, lm))
        tile = add_light(tile, accent, blur_np(lm, 2.0) * 0.18)
    return tile


def slot(w, h, radius=RADIUS_SM, state="off", accent=ACCENT):
    """Inventory / storage / calendar slot tile."""
    if state == "on":
        tile = glass_panel(
            w, h, radius=radius, tint_top=(34, 76, 128), tint_bot=(16, 38, 72),
            alpha_top=0.92, alpha_bot=0.86, border_alpha=0.72, ticks=False,
            inner_glow=0.42, vignette=0.16, noise=0.006,
        )
        tile = add_light(tile, accent, blur_np(ring_mask(w, h, radius, 1.5), 2.6) * 0.60)
    elif state == "lock":
        tile = glass_panel(
            w, h, radius=radius, tint_top=(16, 22, 36), tint_bot=(8, 12, 22),
            alpha_top=0.80, alpha_bot=0.74, border_alpha=0.22, ticks=False,
            inner_glow=0.06, vignette=0.34, noise=0.006,
        )
    else:
        tile = glass_panel(
            w, h, radius=radius, tint_top=(22, 36, 62), tint_bot=(11, 18, 34),
            alpha_top=0.86, alpha_bot=0.80, border_alpha=0.34, ticks=False,
            inner_glow=0.14, vignette=0.24, noise=0.006,
        )
    return tile


def divider(w, h, y, x0=0, x1=None, alpha=0.22, color=BORDER, feather=True):
    """Horizontal hairline that fades out at both ends."""
    x1 = w if x1 is None else x1
    out = np.zeros((h, w, 4), dtype=np.float32)
    v = Vec(w, h)
    v.line([(x0, y + 0.5), (x1, y + 0.5)], width=1.0)
    m = v.mask()
    if feather:
        t = np.linspace(0, 1, w, dtype=np.float32)
        fade = np.clip(np.sin(t * math.pi) * 1.8, 0, 1)[None, :]
        m = m * fade
    out = over(out, layer(w, h, color, m * alpha))
    return out


def text_np(w, h, xy, txt, fnt, color=TEXT, anchor="mm", glow=None, glow_amount=0.30, shadow=0.45):
    out = np.zeros((h, w, 4), dtype=np.float32)
    v = Vec(w, h)
    v.text(xy, txt, fnt, fill=255, anchor=anchor)
    m = v.mask()
    if shadow:
        out = over(out, layer(w, h, (2, 5, 12), blur_np(m, 1.2) * shadow))
    if glow:
        out = over(out, layer(w, h, glow, blur_np(m, 2.4) * glow_amount))
    out = over(out, layer(w, h, color, m))
    return out


def titlebar(w, h, radius=RADIUS, accent=ACCENT):
    """Shared window header strip: glass bar + accent underline."""
    bar = glass_panel(
        w, h, radius=radius, corners=(True, True, False, False),
        tint_top=(30, 52, 92), tint_bot=(14, 24, 44),
        alpha_top=0.88, alpha_bot=0.80, border_alpha=0.42,
        ticks=False, inner_glow=0.20, vignette=0.22,
    )
    # accent underline with falloff
    line = np.zeros((h, w), dtype=np.float32)
    line[h - 1, :] = 1.0
    line[h - 2, :] = 0.55
    fade = np.clip(np.sin(np.linspace(0, math.pi, w, dtype=np.float32)) * 1.7, 0, 1)[None, :]
    bar = add_light(bar, accent, blur_np(line * fade, 2.2) * 0.55)
    bar = over(bar, layer(w, h, accent, line * fade * 0.55))
    return bar


def save(arr, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = to_img(arr) if isinstance(arr, np.ndarray) else arr
    img.save(path, "PNG", optimize=True)
    return path
