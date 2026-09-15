"""Shared vector glyph vocabulary — one function per icon, drawn into a Vec.

Every glyph is authored in a 0..1 unit box and scaled by the caller, so the
same sword reads correctly at 13px on a storage tab and at 40px on a button.
"""

import math


def _p(cx, cy, s, pts):
    return [(cx + x * s, cy + y * s) for x, y in pts]


def potion(v, cx, cy, s, w=None):
    """Consumable / use item — round flask."""
    v.rrect([cx - .11 * s, cy - .50 * s, cx + .11 * s, cy - .30 * s], .04 * s, fill=255)
    v.rrect([cx - .17 * s, cy - .36 * s, cx + .17 * s, cy - .26 * s], .03 * s, fill=255)
    v.ellipse([cx - .34 * s, cy - .22 * s, cx + .34 * s, cy + .46 * s], fill=255)
    v.pieslice([cx - .34 * s, cy - .22 * s, cx + .34 * s, cy + .46 * s], 15, 165, fill=90)


def armor(v, cx, cy, s):
    """Equipment / armor — a shielded cuirass."""
    v.poly(_p(cx, cy, s, [(0, -.50), (.42, -.32), (.42, .08), (0, .50), (-.42, .08), (-.42, -.32)]), fill=255)
    v.poly(_p(cx, cy, s, [(0, -.30), (.24, -.19), (.24, .04), (0, .28), (-.24, .04), (-.24, -.19)]), fill=90)


def card(v, cx, cy, s):
    v.rrect([cx - .28 * s, cy - .46 * s, cx + .28 * s, cy + .46 * s], .09 * s, fill=255)
    v.rrect([cx - .16 * s, cy - .34 * s, cx + .16 * s, cy + .12 * s], .05 * s, fill=70)
    v.line(_p(cx, cy, s, [(-.16, .28), (.16, .28)]), width=max(1.0, .08 * s), fill=70)


def sword(v, cx, cy, s):
    """Weapon — blade + crossguard; the guard is what separates it from ammo."""
    v.poly(_p(cx, cy, s, [(0, -.52), (.13, -.34), (.13, .06), (-.13, .06), (-.13, -.34)]), fill=255)
    v.rrect([cx - .38 * s, cy + .04 * s, cx + .38 * s, cy + .17 * s], .05 * s, fill=255)
    v.rect([cx - .07 * s, cy + .15 * s, cx + .07 * s, cy + .42 * s], fill=255)
    v.ellipse([cx - .12 * s, cy + .36 * s, cx + .12 * s, cy + .54 * s], fill=255)


def arrow_ammo(v, cx, cy, s):
    v.poly(_p(cx, cy, s, [(0, -.50), (.26, -.14), (-.26, -.14)]), fill=255)
    v.rect([cx - .06 * s, cy - .20 * s, cx + .06 * s, cy + .50 * s], fill=255)
    for yy in (.12, .28):
        v.poly(_p(cx, cy, s, [(-.06, yy), (-.32, yy + .16), (-.06, yy + .16)]), fill=255)
        v.poly(_p(cx, cy, s, [(.06, yy), (.32, yy + .16), (.06, yy + .16)]), fill=255)


def box(v, cx, cy, s):
    """Misc / etc."""
    v.poly(_p(cx, cy, s, [(0, -.48), (.44, -.24), (.44, .26), (0, .50), (-.44, .26), (-.44, -.24)]), fill=255)
    v.line(_p(cx, cy, s, [(-.44, -.24), (0, .00), (.44, -.24)]), width=max(1.0, .055 * s), fill=70)
    v.line(_p(cx, cy, s, [(0, .00), (0, .50)]), width=max(1.0, .055 * s), fill=70)


def star(v, cx, cy, s):
    v.star(cx, cy, .50 * s, .21 * s, fill=255)


def shield(v, cx, cy, s):
    v.poly(_p(cx, cy, s, [(0, -.50), (.40, -.32), (.40, .06), (0, .50), (-.40, .06), (-.40, -.32)]), fill=255)


def helmet(v, cx, cy, s):
    v.pieslice([cx - .42 * s, cy - .46 * s, cx + .42 * s, cy + .30 * s], 180, 360, fill=255)
    v.rrect([cx - .42 * s, cy - .10 * s, cx + .42 * s, cy + .12 * s], .06 * s, fill=255)
    v.rect([cx - .14 * s, cy - .06 * s, cx + .42 * s, cy + .06 * s], fill=0)


def body(v, cx, cy, s):
    v.ellipse([cx - .17 * s, cy - .50 * s, cx + .17 * s, cy - .16 * s], fill=255)
    v.rrect([cx - .30 * s, cy - .14 * s, cx + .30 * s, cy + .24 * s], .10 * s, fill=255)
    v.rrect([cx - .26 * s, cy + .20 * s, cx - .05 * s, cy + .52 * s], .07 * s, fill=255)
    v.rrect([cx + .05 * s, cy + .20 * s, cx + .26 * s, cy + .52 * s], .07 * s, fill=255)


def ring(v, cx, cy, s):
    """Accessory."""
    v.ellipse([cx - .34 * s, cy - .18 * s, cx + .34 * s, cy + .48 * s], outline=255, width=max(1.0, .11 * s))
    v.poly(_p(cx, cy, s, [(0, -.50), (.18, -.28), (0, -.12), (-.18, -.28)]), fill=255)


def dress(v, cx, cy, s):
    """Costume."""
    v.poly(_p(cx, cy, s, [(-.16, -.46), (.16, -.46), (.34, -.20), (.22, -.10), (.34, .46), (-.34, .46), (-.22, -.10),
                          (-.34, -.20)]), fill=255)


def check(v, cx, cy, s, w=None):
    v.line(_p(cx, cy, s, [(-.34, .02), (-.10, .28), (.36, -.28)]), width=w or max(1.2, .18 * s))


def cross(v, cx, cy, s, w=None):
    ww = w or max(1.2, .16 * s)
    v.line(_p(cx, cy, s, [(-.30, -.30), (.30, .30)]), width=ww)
    v.line(_p(cx, cy, s, [(.30, -.30), (-.30, .30)]), width=ww)


def plus(v, cx, cy, s, w=None):
    ww = w or max(1.2, .16 * s)
    v.line(_p(cx, cy, s, [(-.34, 0), (.34, 0)]), width=ww)
    v.line(_p(cx, cy, s, [(0, -.34), (0, .34)]), width=ww)


def magnifier(v, cx, cy, s):
    r = .30 * s
    v.ellipse([cx - r - .05 * s, cy - r - .05 * s, cx + r - .05 * s, cy + r - .05 * s],
              outline=255, width=max(1.2, .12 * s))
    v.line([(cx + r * .60, cy + r * .60), (cx + .46 * s, cy + .46 * s)], width=max(1.4, .14 * s))


def lock(v, cx, cy, s):
    v.arc([cx - .26 * s, cy - .48 * s, cx + .26 * s, cy + .06 * s], 180, 360, width=max(1.2, .12 * s))
    v.rrect([cx - .34 * s, cy - .12 * s, cx + .34 * s, cy + .44 * s], .10 * s, fill=255)
    v.ellipse([cx - .07 * s, cy + .06 * s, cx + .07 * s, cy + .20 * s], fill=40)


def gear(v, cx, cy, s):
    for i in range(8):
        a = math.radians(i * 45)
        x, y = cx + math.cos(a) * .40 * s, cy + math.sin(a) * .40 * s
        v.ellipse([x - .11 * s, y - .11 * s, x + .11 * s, y + .11 * s], fill=255)
    v.ellipse([cx - .30 * s, cy - .30 * s, cx + .30 * s, cy + .30 * s], fill=255)
    v.ellipse([cx - .12 * s, cy - .12 * s, cx + .12 * s, cy + .12 * s], fill=0)


def coin(v, cx, cy, s):
    v.ellipse([cx - .44 * s, cy - .44 * s, cx + .44 * s, cy + .44 * s], fill=255)
    v.ellipse([cx - .30 * s, cy - .30 * s, cx + .30 * s, cy + .30 * s], outline=60, width=max(1.0, .07 * s))


def cart(v, cx, cy, s):
    v.line(_p(cx, cy, s, [(-.46, -.34), (-.28, -.34)]), width=max(1.2, .11 * s))
    v.poly(_p(cx, cy, s, [(-.28, -.34), (.46, -.34), (.34, .06), (-.16, .06)]), fill=255)
    v.ellipse([cx - .18 * s, cy + .20 * s, cx - .02 * s, cy + .36 * s], fill=255)
    v.ellipse([cx + .16 * s, cy + .20 * s, cx + .32 * s, cy + .36 * s], fill=255)


def gift(v, cx, cy, s):
    v.rrect([cx - .42 * s, cy - .20 * s, cx + .42 * s, cy + .44 * s], .06 * s, fill=255)
    v.rrect([cx - .46 * s, cy - .34 * s, cx + .46 * s, cy - .14 * s], .05 * s, fill=255)
    v.rect([cx - .08 * s, cy - .34 * s, cx + .08 * s, cy + .44 * s], fill=60)
    v.arc([cx - .34 * s, cy - .52 * s, cx - .00 * s, cy - .22 * s], 0, 250, width=max(1.2, .10 * s))
    v.arc([cx + .00 * s, cy - .52 * s, cx + .34 * s, cy - .22 * s], 290, 180, width=max(1.2, .10 * s))


def download(v, cx, cy, s):
    """Deposit."""
    v.line(_p(cx, cy, s, [(0, -.44), (0, .14)]), width=max(1.2, .13 * s))
    v.poly(_p(cx, cy, s, [(0, .34), (.24, .04), (-.24, .04)]), fill=255)
    v.line(_p(cx, cy, s, [(-.36, .46), (.36, .46)]), width=max(1.2, .11 * s))


def upload(v, cx, cy, s):
    """Withdraw."""
    v.line(_p(cx, cy, s, [(0, .40), (0, -.14)]), width=max(1.2, .13 * s))
    v.poly(_p(cx, cy, s, [(0, -.38), (.24, -.08), (-.24, -.08)]), fill=255)
    v.line(_p(cx, cy, s, [(-.36, -.46), (.36, -.46)]), width=max(1.2, .11 * s))


def sort(v, cx, cy, s):
    v.line(_p(cx, cy, s, [(-.22, -.42), (-.22, .42)]), width=max(1.2, .11 * s))
    v.poly(_p(cx, cy, s, [(-.22, .48), (-.02, .16), (-.42, .16)]), fill=255)
    v.line(_p(cx, cy, s, [(.22, .42), (.22, -.42)]), width=max(1.2, .11 * s))
    v.poly(_p(cx, cy, s, [(.22, -.48), (.42, -.16), (.02, -.16)]), fill=255)


def trash(v, cx, cy, s):
    v.rrect([cx - .30 * s, cy - .24 * s, cx + .30 * s, cy + .46 * s], .08 * s, fill=255)
    v.rrect([cx - .40 * s, cy - .36 * s, cx + .40 * s, cy - .24 * s], .05 * s, fill=255)
    v.rrect([cx - .13 * s, cy - .46 * s, cx + .13 * s, cy - .34 * s], .04 * s, fill=255)
    for dx in (-.12, 0, .12):
        v.line(_p(cx, cy, s, [(dx, -.12), (dx, .34)]), width=max(1.0, .05 * s), fill=50)


def scroll_icon(v, cx, cy, s):
    v.rrect([cx - .26 * s, cy - .34 * s, cx + .26 * s, cy + .34 * s], .06 * s, fill=255)
    v.rrect([cx - .38 * s, cy - .42 * s, cx - .22 * s, cy + .42 * s], .07 * s, fill=200)
    v.rrect([cx + .22 * s, cy - .42 * s, cx + .38 * s, cy + .42 * s], .07 * s, fill=200)
    for i, yy in enumerate((-.16, -.02, .12)):
        v.line(_p(cx, cy, s, [(-.16, yy), (.16 - i * .05 * s / max(s, 1), yy)]), width=max(1.0, .05 * s), fill=60)


def calendar(v, cx, cy, s):
    v.rrect([cx - .42 * s, cy - .34 * s, cx + .42 * s, cy + .44 * s], .09 * s, fill=255)
    v.rect([cx - .42 * s, cy - .34 * s, cx + .42 * s, cy - .14 * s], fill=180)
    v.rrect([cx - .26 * s, cy - .48 * s, cx - .16 * s, cy - .24 * s], .04 * s, fill=255)
    v.rrect([cx + .16 * s, cy - .48 * s, cx + .26 * s, cy - .24 * s], .04 * s, fill=255)
    for r in range(2):
        for c in range(3):
            x = cx + (c - 1) * .24 * s
            y = cy + .02 * s + r * .22 * s
            v.rect([x - .07 * s, y - .06 * s, x + .07 * s, y + .06 * s], fill=60)


def flag(v, cx, cy, s):
    v.line(_p(cx, cy, s, [(-.26, -.48), (-.26, .50)]), width=max(1.2, .11 * s))
    v.poly(_p(cx, cy, s, [(-.20, -.44), (.40, -.24), (-.20, -.04)]), fill=255)


def quill(v, cx, cy, s):
    v.poly(_p(cx, cy, s, [(.44, -.46), (.10, .04), (-.16, .30), (-.30, .16), (-.04, -.10)]), fill=255)
    v.line(_p(cx, cy, s, [(-.20, .26), (-.44, .48)]), width=max(1.2, .10 * s))


def sparkle(v, cx, cy, s):
    v.star(cx, cy, .50 * s, .14 * s, points=4, fill=255)
    v.star(cx + .34 * s, cy - .32 * s, .18 * s, .05 * s, points=4, fill=255)


def clock(v, cx, cy, s):
    v.ellipse([cx - .46 * s, cy - .46 * s, cx + .46 * s, cy + .46 * s], outline=255, width=max(1.2, .10 * s))
    v.line(_p(cx, cy, s, [(0, 0), (0, -.28)]), width=max(1.2, .09 * s))
    v.line(_p(cx, cy, s, [(0, 0), (.22, .10)]), width=max(1.2, .09 * s))


def anvil(v, cx, cy, s):
    v.poly(_p(cx, cy, s, [(-.46, -.26), (.30, -.26), (.46, -.10), (.16, .02), (.16, .20), (-.20, .20), (-.20, .02),
                          (-.46, -.06)]), fill=255)
    v.rrect([cx - .34 * s, cy + .18 * s, cx + .34 * s, cy + .42 * s], .05 * s, fill=255)


def person(v, cx, cy, s):
    v.ellipse([cx - .19 * s, cy - .46 * s, cx + .19 * s, cy - .08 * s], fill=255)
    v.pieslice([cx - .38 * s, cy - .02 * s, cx + .38 * s, cy + .66 * s], 180, 360, fill=255)


def refresh(v, cx, cy, s):
    v.arc([cx - .40 * s, cy - .40 * s, cx + .40 * s, cy + .40 * s], 40, 330, width=max(1.3, .12 * s))
    v.poly(_p(cx, cy, s, [(.40, -.34), (.46, .04), (.10, -.10)]), fill=255)
