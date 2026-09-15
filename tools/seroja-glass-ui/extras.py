"""The extended component set drawn on the concept sheet.

These are NOT in ASSETS.md — they're the extra tabs, slots, stamps, badges and
icons shown in the reference mock-up. They go in <section>/extra/ so the
exact-size drop-in replacements stay unambiguous.
Sizes are chosen to match the concept sheet's proportions.
"""

import math
import os

import numpy as np

import glass as g
import icons as ic
from glass import (ACCENT, ACCENT2, BORDER, DANGER, GOLD, MUTED, SUCCESS, TEXT,
                   VIOLET, Vec, add_light, blur_np, layer, mask_to_np, over,
                   paste, ring_mask, rr_mask, vgrad)

ROOT = os.environ.get("OUT", "../p22/P22/new-assets")


# ------------------------------------------------------------- primitives ---
def panel(w, h, r=g.RADIUS, **kw):
    kw.setdefault("tint_top", (24, 42, 78))
    kw.setdefault("tint_bot", (9, 15, 30))
    kw.setdefault("alpha_top", 0.70)
    kw.setdefault("alpha_bot", 0.60)
    kw.setdefault("border_alpha", 0.50)
    kw.setdefault("inner_glow", 0.28)
    return g.glass_panel(w, h, radius=r, **kw)


def icon_button(w, h, draw, tone="blue", state="normal", r=g.RADIUS_SM, scale=0.54, accent=None):
    tile = g.button(w, h, radius=r, tone=tone, state=state)
    v = Vec(w, h)
    draw(v, w / 2.0, h / 2.0, min(w, h) * scale)
    m = v.mask()
    tile = over(tile, layer(w, h, (2, 6, 14), blur_np(m, 1.2) * 0.40))
    glow = accent or {"blue": ACCENT, "green": SUCCESS, "red": DANGER,
                      "gold": GOLD, "violet": VIOLET, "ghost": ACCENT}[tone]
    tile = add_light(tile, glow, blur_np(m, 2.6) * 0.45)
    tile = over(tile, layer(w, h, (238, 248, 255), m * 0.96))
    return tile


def round_icon(d, draw, tone=ACCENT, fill=(18, 32, 58), scale=0.50, ring_a=0.75):
    w = h = d
    out = np.zeros((h, w, 4), dtype=np.float32)
    disc = mask_to_np(g.ellipse_mask(w, h, [0.8, 0.8, w - 0.8, h - 0.8]))
    out = over(out, layer(w, h, tone, blur_np(disc, d * 0.18) * 0.32))
    out = over(out, layer(w, h, fill, disc * 0.94))
    out = add_light(out, tone, disc * vgrad(h, w, 0.22, 0.0) * 0.5)
    rg = np.clip(disc - mask_to_np(g.ellipse_mask(w, h, [0.8, 0.8, w - 0.8, h - 0.8], inset=1.3)), 0, 1)
    out = add_light(out, tone, blur_np(rg, 2.4) * 0.55)
    out = over(out, layer(w, h, (196, 230, 255), rg * ring_a))
    v = Vec(w, h)
    draw(v, w / 2.0, h / 2.0, d * scale)
    m = v.mask()
    out = add_light(out, tone, blur_np(m, 2.2) * 0.45)
    out = over(out, layer(w, h, (240, 250, 255), m * 0.96))
    return out


def tab_bar(w, h, on, label=None, accent=ACCENT):
    if on:
        t = g.glass_panel(w, h, radius=g.RADIUS_SM, tint_top=(36, 76, 130), tint_bot=(18, 40, 76),
                          alpha_top=0.95, alpha_bot=0.90, border_alpha=0.70, ticks=False,
                          inner_glow=0.40, vignette=0.16)
        t = add_light(t, accent, blur_np(ring_mask(w, h, g.RADIUS_SM, 1.4), 3.0) * 0.55)
    else:
        t = g.glass_panel(w, h, radius=g.RADIUS_SM, tint_top=(18, 30, 54), tint_bot=(9, 15, 29),
                          alpha_top=0.80, alpha_bot=0.74, border_alpha=0.28, ticks=False,
                          inner_glow=0.10, vignette=0.24)
    if label:
        t = over(t, g.text_np(w, h, (w / 2, h / 2), label, g.font("ui_b", max(9, int(h * 0.40))),
                              color=TEXT if on else MUTED, glow=accent if on else None, glow_amount=0.25))
    return t


def badge(w, h, text, tone, accent):
    t = g.button(w, h, radius=8, tone=tone, state="on")
    t = over(t, g.text_np(w, h, (w / 2, h / 2 - 1), text, g.font("ui_b", int(h * 0.62)),
                          color=(250, 252, 255), glow=accent, glow_amount=0.45, shadow=0.55))
    return t


def emit(section, items):
    d = os.path.join(ROOT, section, "extra")
    for name, arr in items.items():
        g.save(arr, os.path.join(d, name))
    print(f"  {section}/extra: {len(items)} files")
    return len(items)


# ------------------------------------------------------------------ build ---
def build_cashshop():
    items = {}
    items["bg_tab.png"] = tab_bar(176, 40, False)
    items["bg_tab_on.png"] = tab_bar(176, 40, True)
    items["bg_item.png"] = panel(176, 64, r=12, ticks=False)
    hov = panel(176, 64, r=12, ticks=False, tint_top=(34, 68, 118), tint_bot=(14, 26, 50),
                alpha_top=0.82, alpha_bot=0.72, border_alpha=0.68, inner_glow=0.40)
    items["bg_item_hover.png"] = add_light(hov, ACCENT, blur_np(ring_mask(176, 64, 12, 1.4), 3.2) * 0.50)
    items["bg_preview.png"] = panel(176, 64, r=12, ticks=True)
    items["btn_buy.png"] = icon_button(44, 34, ic.cart, tone="blue", state="on")
    items["btn_gift.png"] = icon_button(44, 34, ic.gift, tone="violet", state="on")
    items["btn_cart.png"] = icon_button(44, 34, ic.cart, tone="ghost")
    cur = panel(92, 26, r=9, ticks=False, tint_top=(30, 40, 60), tint_bot=(12, 16, 28),
                alpha_top=0.88, alpha_bot=0.82, border_alpha=0.42, inner_glow=0.18)
    cur = add_light(cur, GOLD, blur_np(ring_mask(92, 26, 9, 1.2), 2.8) * 0.28)
    v = Vec(92, 26)
    ic.coin(v, 14, 13, 15)
    m = v.mask()
    cur = add_light(cur, GOLD, blur_np(m, 2.4) * 0.55)
    cur = over(cur, layer(92, 26, (255, 232, 170), m * 0.95))
    items["currency_bg.png"] = cur
    items["cash_icon.png"] = round_icon(28, lambda v, x, y, s: v.text((x, y + .5), "C", g.font("ui_b", int(s * 1.5))),
                                        tone=ACCENT)
    items["mileage_icon.png"] = round_icon(28, lambda v, x, y, s: v.text((x, y + .5), "M", g.font("ui_b", int(s * 1.5))),
                                           tone=VIOLET)
    return emit("cashshop", items)


def build_attendance():
    items = {}
    items["bg_calendar.png"] = panel(176, 72, r=12)
    items["bg_reward_panel.png"] = panel(176, 56, r=12, ticks=False)
    items["bg_info.png"] = panel(176, 44, r=10, ticks=False, alpha_top=0.60, alpha_bot=0.52)
    items["stamp_empty.png"] = g.slot(44, 44, state="lock")
    chk = g.slot(44, 44, state="off")
    v = Vec(44, 44)
    ic.check(v, 22, 22, 30, w=4.2)
    m = v.mask()
    chk = add_light(chk, SUCCESS, blur_np(m, 3.0) * 0.70)
    chk = over(chk, layer(44, 44, (198, 255, 224), m * 0.95))
    items["stamp_checked.png"] = chk
    tod = g.slot(44, 44, state="on")
    v2 = Vec(44, 44)
    ic.plus(v2, 22, 22, 22, w=3.2)
    m2 = v2.mask()
    tod = add_light(tod, ACCENT, blur_np(m2, 3.0) * 0.75)
    tod = over(tod, layer(44, 44, (240, 250, 255), m2 * 0.96))
    items["stamp_today.png"] = tod
    items["reward_box.png"] = icon_button(44, 44, ic.gift, tone="gold", state="on", r=g.RADIUS_SM, scale=0.58)
    claimed = icon_button(44, 44, ic.gift, tone="ghost", state="off", r=g.RADIUS_SM, scale=0.58)
    v3 = Vec(44, 44)
    ic.check(v3, 32, 32, 20, w=3.0)
    m3 = v3.mask()
    claimed = add_light(claimed, SUCCESS, blur_np(m3, 2.6) * 0.65)
    claimed = over(claimed, layer(44, 44, (198, 255, 224), m3 * 0.95))
    items["reward_claimed.png"] = claimed
    items["btn_claim.png"] = g.button(92, 28, radius=9, tone="green", state="on", label="CLAIM", font_size=12)
    return emit("check_attendance", items)


def build_enchant():
    items = {}
    items["bg_main.png"] = panel(240, 180)
    items["bg_tab.png"] = tab_bar(176, 40, False)
    items["bg_material.png"] = panel(176, 56, r=12, ticks=False)
    items["bg_result.png"] = panel(176, 56, r=12, ticks=False)
    items["btn_enchant.png"] = icon_button(72, 30, ic.anvil, tone="blue", state="on", scale=0.62)
    items["btn_reset.png"] = icon_button(72, 30, ic.refresh, tone="ghost", scale=0.58)
    items["btn_cancel.png"] = icon_button(72, 30, ic.cross, tone="red", scale=0.50)
    tones = [("blue", ACCENT), ("blue", ACCENT2), ("green", SUCCESS), ("violet", VIOLET), ("gold", GOLD)]
    for i, (tone, acc) in enumerate(tones, start=1):
        items[f"grade_{i}.png"] = badge(40, 26, f"+{i}", tone, acc)
    return emit("enchant_grade", items)


def build_equipdoll():
    items = {}
    items["bg_slot.png"] = g.slot(44, 44, state="off")
    items["bg_slot_on.png"] = g.slot(44, 44, state="on")
    lock = g.slot(44, 44, state="lock")
    v = Vec(44, 44)
    ic.lock(v, 22, 22, 22)
    m = v.mask()
    lock = over(lock, layer(44, 44, MUTED, m * 0.50))
    items["bg_slot_lock.png"] = lock
    items["bg_tab.png"] = tab_bar(176, 40, False)
    prev = panel(116, 96, r=12, ticks=True, alpha_top=0.50, alpha_bot=0.42)
    import s7_equipdoll as s7
    prev = over(prev, s7.doll_bg(116, 96, "general"))
    items["bg_doll_preview.png"] = prev
    for name, glyph in (("head", ic.helmet), ("body", ic.armor), ("weapon", ic.sword),
                        ("shield", ic.shield), ("accessory", ic.ring), ("costume", ic.dress)):
        tile = g.slot(44, 44, state="off")
        v2 = Vec(44, 44)
        glyph(v2, 22, 22, 24)
        m2 = v2.mask()
        tile = over(tile, layer(44, 44, (2, 6, 14), blur_np(m2, 1.2) * 0.35))
        tile = add_light(tile, ACCENT, blur_np(m2, 2.6) * 0.35)
        tile = over(tile, layer(44, 44, (190, 216, 244), m2 * 0.80))
        items[f"slot_{name}.png"] = tile
    return emit("equipment_doll", items)


def build_quest():
    items = {}
    items["bg_tab.png"] = tab_bar(176, 40, False)
    items["bg_list.png"] = panel(176, 64, r=12, ticks=False)
    items["bg_detail.png"] = panel(176, 64, r=12, ticks=True)
    for name, glyph, tone in (("main", ic.quill, ACCENT), ("sub", ic.scroll_icon, ACCENT2),
                              ("daily", ic.calendar, VIOLET), ("event", ic.sparkle, GOLD),
                              ("complete", ic.check, SUCCESS)):
        items[f"icon_{name}.png"] = round_icon(40, glyph, tone=tone, scale=0.48)
    items["btn_navigate.png"] = icon_button(72, 30, lambda v, x, y, s: v.poly(
        [(x - s * .22, y - s * .30), (x + s * .30, y), (x - s * .22, y + s * .30)], fill=255),
        tone="blue", state="on")
    items["btn_abandon.png"] = icon_button(72, 30, ic.trash, tone="red", scale=0.52)
    return emit("quest", items)


def build_storage():
    items = {}
    items["bg_window.png"] = panel(240, 180)
    items["bg_tab.png"] = tab_bar(176, 40, False)
    items["bg_slot.png"] = g.slot(40, 40, state="off")
    items["bg_slot_on.png"] = g.slot(40, 40, state="on")
    items["btn_deposit.png"] = icon_button(44, 34, ic.download, tone="blue", state="on")
    items["btn_withdraw.png"] = icon_button(44, 34, ic.upload, tone="blue", state="on")
    items["btn_sort.png"] = icon_button(44, 34, ic.sort, tone="ghost")
    items["btn_search.png"] = icon_button(44, 34, ic.magnifier, tone="ghost")
    items["btn_lock.png"] = icon_button(44, 34, ic.lock, tone="gold", state="on")
    items["slot_expand.png"] = icon_button(40, 40, ic.plus, tone="green", state="on", scale=0.46)
    return emit("storage_tabs", items)


def build_login():
    items = {}
    logo = np.zeros((34, 120, 4), dtype=np.float32)
    logo = over(logo, g.text_np(120, 34, (60, 15), "SeROja", g.font("display", 28),
                                color=(226, 240, 255), glow=ACCENT, glow_amount=0.50, shadow=0.55))
    logo = over(logo, g.text_np(120, 34, (60, 29), "R A G N A R O K   O N L I N E", g.font("tech", 6),
                                color=MUTED, glow=None, shadow=0.35))
    items["logo_top.png"] = logo
    items["btn_login.png"] = g.button(132, 30, radius=g.RADIUS_SM, tone="blue", state="on",
                                      label="LOGIN", font_size=14)
    items["btn_exit.png"] = icon_button(44, 30, ic.cross, tone="red", scale=0.42)
    items["btn_settings.png"] = icon_button(44, 30, ic.gear, tone="ghost", scale=0.50)
    cb = g.glass_panel(20, 20, radius=5, tint_top=(26, 48, 86), tint_bot=(12, 22, 42),
                       alpha_top=0.90, alpha_bot=0.84, border_alpha=0.55, ticks=False,
                       inner_glow=0.26, vignette=0.16)
    v = Vec(20, 20)
    ic.check(v, 10, 10, 15, w=2.4)
    m = v.mask()
    cb = add_light(cb, ACCENT, blur_np(m, 2.2) * 0.60)
    cb = over(cb, layer(20, 20, (238, 249, 255), m * 0.96))
    items["checkbox.png"] = cb
    for name, tone in (("server_status_on", SUCCESS), ("server_status_off", DANGER)):
        w = h = 20
        out = np.zeros((h, w, 4), dtype=np.float32)
        disc = mask_to_np(g.ellipse_mask(w, h, [4.0, 4.0, w - 4.0, h - 4.0]))
        out = over(out, layer(w, h, tone, blur_np(disc, 3.4) * 0.62))
        out = over(out, layer(w, h, tone, disc * 0.95))
        hi = mask_to_np(g.ellipse_mask(w, h, [6.0, 5.4, 10.4, 9.0]))
        out = add_light(out, (255, 255, 255), hi * 0.50)
        items[f"{name}.png"] = out
    well = np.zeros((26, 132, 4), dtype=np.float32)
    items["bg_input.png"] = over(well, g.inset_well(132, 26, (0, 0, 132, 26), radius=8,
                                                    fill=(7, 12, 25), fill_alpha=0.70,
                                                    depth=0.36, border_alpha=0.40, glow=0.10))
    items["bg_server_list.png"] = panel(132, 40, r=9, ticks=False, alpha_top=0.72, alpha_bot=0.64)
    items["bg_button.png"] = g.button(132, 26, radius=8, tone="ghost")
    return emit("win_login", items)


if __name__ == "__main__":
    n = 0
    for fn in (build_cashshop, build_attendance, build_enchant, build_equipdoll,
               build_quest, build_storage, build_login):
        n += fn()
    print(f"extras: {n} files")
