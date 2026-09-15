"""Contact-sheet preview of a generated section, on the real world background."""

import os
import sys

import numpy as np
from PIL import Image

import glass as g

ROOT = os.environ.get("OUT", "../p22/P22/new-assets")
PREV = "../preview"


def sheet(section, cols=None, pad=14, maxw=1500):
    d = os.path.join(ROOT, section)
    files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    imgs = [(f, Image.open(os.path.join(d, f)).convert("RGBA")) for f in files]
    # simple shelf packing
    rows, cur, curw, rowh = [], [], 0, 0
    for f, im in imgs:
        wlab = max(im.width, 90)
        if cur and curw + wlab + pad > maxw:
            rows.append((cur, rowh))
            cur, curw, rowh = [], 0, 0
        cur.append((f, im))
        curw += wlab + pad
        rowh = max(rowh, im.height)
    if cur:
        rows.append((cur, rowh))
    W = min(maxw, max(sum(max(im.width, 90) + pad for _, im in r) + pad for r, _ in rows))
    H = sum(rh + 26 + pad for _, rh in rows) + pad + 26
    out = np.zeros((H, W, 4), dtype=np.float32)
    out[..., :3] = np.asarray(g.BG, dtype=np.float32) / 255.0
    out[..., 3] = 1.0
    # checker so alpha is visible
    yy, xx = np.mgrid[0:H, 0:W]
    ch = (((xx // 8) + (yy // 8)) % 2).astype(np.float32) * 0.035
    out[..., :3] += ch[..., None]

    f14 = g.font("ui_b", 13)
    f10 = g.font("tech", 11)
    out = g.paste(out, g.text_np(W, 26, (10, 13), f"{section}", f14, color=g.ACCENT, anchor="lm", shadow=0), 0, 2)
    y = 26 + pad
    for r, rh in rows:
        x = pad
        for f, im in r:
            tile = g.to_np(im)
            out = g.paste(out, tile, x, y + (rh - im.height) // 2)
            lab = g.text_np(max(im.width, 90) + 40, 20, (0, 10), f"{f}  {im.width}x{im.height}",
                            f10, color=g.MUTED, anchor="lm", shadow=0)
            out = g.paste(out, lab, x, y + rh + 4)
            x += max(im.width, 90) + pad
        y += rh + 26 + pad
    os.makedirs(PREV, exist_ok=True)
    p = os.path.join(PREV, f"sheet_{section}.png")
    g.save(out, p)
    print(p)
    return p


if __name__ == "__main__":
    for s in sys.argv[1:]:
        sheet(s)
