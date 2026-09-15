# SeROja Glass UI — replacement art

Generated against `PROMPT.md` / `ASSETS.md` in this same folder.

**151 PNGs**, all RGBA with real alpha:

- **78 exact-size drop-in replacements** — one for every file in
  `current-assets/` except `misc_chrome_reference/` (explicitly out of scope).
  Every one is byte-for-byte the same canvas size as the file it replaces;
  verified programmatically, zero mismatches.
- **73 additional components** in each section's `extra/` subfolder — the tabs,
  slots, stamps, badges and icons from the concept sheet that `ASSETS.md`
  doesn't list. Kept separate so the drop-in set stays unambiguous.

## Format notes

Files whose originals were `.bmp` or `.tga` ship as `.png` with the same stem,
per `ASSETS.md` ("PNG is fine even where the original was `.bmp`/`.tga` — I'll
wire the extension change into the code"). Affected files:

```
check_attendance/bt_slot_a.bmp        -> bt_slot_a.png
check_attendance/bt_slot_off.tga      -> bt_slot_off.png
check_attendance/bt_slot_complete.tga -> bt_slot_complete.png
enchant_grade/bg_grade_enchant.bmp    -> bg_grade_enchant.png
enchant_grade/btn_start.bmp           -> btn_start.png
enchant_grade/btn_unbroken_over.bmp   -> btn_unbroken_over.png
enchant_grade/btn_unbroken_pick.bmp   -> btn_unbroken_pick.png
quest/img_questiocn.bmp               -> img_questiocn.png
quest/quest_window.bmp                -> quest_window.png
win_login/bg_login.tga                -> bg_login.png
equipment_doll/equipwin_bg2.bmp       -> equipwin_bg2.png
storage_tabs/tab_itm_01..03.bmp       -> tab_itm_01..03.png
```

The GRF-extracted BMP/TGA originals used magenta `#FF00FF` as their colour key;
the replacements use genuine alpha instead, so no keying step is needed.

## Palette

Every asset uses the `glassTheme.css` tokens verbatim — `#060a14` ground,
`rgba(18,30,54,.55)` glass, `rgba(148,197,255,.22/.4)` borders, `#4fc3f7` accent,
`#eaf2ff` / `#8fa3c4` text, `#ff5c5c` danger, `#4ade80` success, 16px / 10px radii.

## Structural fidelity

Backgrounds that the client pixel-positions things onto keep the original's
internal geometry, measured off the old bitmaps rather than eyeballed:

| window | preserved geometry |
|---|---|
| Cash Shop | promo banner `x10..530 y18..70`; 3×3 item cards `x(11,186,361)+166 y(108,235,363)+121`; cart rail at `x534`; 6 cart rows `y(5,62,119,176,233,290)+49` |
| Check Attendance | 20 day cells `x(27,89,151,213,275)+56 y(96,160,224,288)+58`; right rail `x340..470`; OK tray below `y360` |
| Quest | tab rail `x0..30`, bands `y18-115 / 119-216 / 220-317 / 321-418` |
| Login | server row `x14..171 y11..30` (chevron well `x151..170`), user `y38..56`, pass `y62..80`, checkbox `x58..68 y85..95`, Login disc centred `(238,72) r45`, close X `(283,22) r10.5` |
| Enchant Grade | altar column `x0..140`, UI panel `x140..400` |

## Manifest

### `achievement/` — 12 drop-in replacements

| new file | size | replaces |
|---|---|---|
| `bg_detail.png` | 328×405 | `bg_detail.png` |
| `bg_list.png` | 309×405 | `bg_list.png` |
| `bg_summary.png` | 648×404 | `bg_summary.png` |
| `bg_tab.png` | 102×405 | `bg_tab.png` |
| `bg_upper.png` | 750×46 | `bg_upper.png` |
| `btn_radio_off.png` | 12×12 | `btn_radio_off.png` |
| `btn_radio_on.png` | 12×12 | `btn_radio_on.png` |
| `detail_stamp.png` | 64×54 | `detail_stamp.png` |
| `reward_buff.png` | 62×62 | `reward_buff.png` |
| `reward_item.png` | 62×62 | `reward_item.png` |
| `reward_title.png` | 62×62 | `reward_title.png` |
| `upper_trophy.png` | 39×40 | `upper_trophy.png` |

### `cashshop/` — 31 drop-in replacements

| new file | size | replaces |
|---|---|---|
| `bt_arrowL2_off.png` | 16×12 | `bt_arrowL2_off.png` |
| `bt_arrowL2_on.png` | 16×12 | `bt_arrowL2_on.png` |
| `bt_arrowL_off.png` | 11×12 | `bt_arrowL_off.png` |
| `bt_arrowL_on.png` | 11×12 | `bt_arrowL_on.png` |
| `bt_arrowR2_off.png` | 16×12 | `bt_arrowR2_off.png` |
| `bt_arrowR2_on.png` | 16×12 | `bt_arrowR2_on.png` |
| `bt_arrowR_off.png` | 11×12 | `bt_arrowR_off.png` |
| `bt_arrowR_on.png` | 11×12 | `bt_arrowR_on.png` |
| `btn_buy_normal.png` | 154×23 | `btn_buy_normal.png` |
| `btn_charge_normal.png` | 64×20 | `btn_charge_normal.png` |
| `btn_searchbar_normal.png` | 54×18 | `btn_searchbar_normal.png` |
| `img_shop_bg.png` | 723×540 | `img_shop_bg.png` |
| `img_shop_cart_bg.png` | 185×350 | `img_shop_cart_bg.png` |
| `img_shop_tap0_off.png` | 56×31 | `img_shop_tap0_off.png` |
| `img_shop_tap0_on.png` | 56×31 | `img_shop_tap0_on.png` |
| `img_shop_tap1_off.png` | 56×31 | `img_shop_tap1_off.png` |
| `img_shop_tap1_on.png` | 56×31 | `img_shop_tap1_on.png` |
| `img_shop_tap2_off.png` | 56×31 | `img_shop_tap2_off.png` |
| `img_shop_tap2_on.png` | 56×31 | `img_shop_tap2_on.png` |
| `img_shop_tap3_off.png` | 56×31 | `img_shop_tap3_off.png` |
| `img_shop_tap3_on.png` | 56×31 | `img_shop_tap3_on.png` |
| `img_shop_tap4_off.png` | 56×31 | `img_shop_tap4_off.png` |
| `img_shop_tap4_on.png` | 56×31 | `img_shop_tap4_on.png` |
| `img_shop_tap5_off.png` | 56×31 | `img_shop_tap5_off.png` |
| `img_shop_tap5_on.png` | 56×31 | `img_shop_tap5_on.png` |
| `img_shop_tap6_off.png` | 56×31 | `img_shop_tap6_off.png` |
| `img_shop_tap6_on.png` | 56×31 | `img_shop_tap6_on.png` |
| `img_shop_tap7_off.png` | 56×31 | `img_shop_tap7_off.png` |
| `img_shop_tap7_on.png` | 56×31 | `img_shop_tap7_on.png` |
| `img_shop_tap8_off.png` | 56×31 | `img_shop_tap8_off.png` |
| `img_shop_tap8_on.png` | 56×31 | `img_shop_tap8_on.png` |

`cashshop/extra/` — 11 additional components (not in ASSETS.md; from the concept sheet): `bg_item.png` 176×64, `bg_item_hover.png` 176×64, `bg_preview.png` 176×64, `bg_tab.png` 176×40, `bg_tab_on.png` 176×40, `btn_buy.png` 44×34, `btn_cart.png` 44×34, `btn_gift.png` 44×34, `cash_icon.png` 28×28, `currency_bg.png` 92×26, `mileage_icon.png` 28×28

### `check_attendance/` — 6 drop-in replacements

| new file | size | replaces |
|---|---|---|
| `attendance_bg.png` | 488×413 | `attendance_bg.png` |
| `bt_ok_normal.png` | 146×30 | `bt_ok_normal.png` |
| `bt_ok_press.png` | 146×30 | `bt_ok_press.png` |
| `bt_slot_a.png` | 58×60 | `bt_slot_a.bmp` *(was BMP/TGA)* |
| `bt_slot_complete.png` | 58×60 | `bt_slot_complete.tga` *(was BMP/TGA)* |
| `bt_slot_off.png` | 58×60 | `bt_slot_off.tga` *(was BMP/TGA)* |

`check_attendance/extra/` — 9 additional components (not in ASSETS.md; from the concept sheet): `bg_calendar.png` 176×72, `bg_info.png` 176×44, `bg_reward_panel.png` 176×56, `btn_claim.png` 92×28, `reward_box.png` 44×44, `reward_claimed.png` 44×44, `stamp_checked.png` 44×44, `stamp_empty.png` 44×44, `stamp_today.png` 44×44

### `enchant_grade/` — 4 drop-in replacements

| new file | size | replaces |
|---|---|---|
| `bg_grade_enchant.png` | 400×330 | `bg_grade_enchant.bmp` *(was BMP/TGA)* |
| `btn_start.png` | 82×28 | `btn_start.bmp` *(was BMP/TGA)* |
| `btn_unbroken_over.png` | 28×40 | `btn_unbroken_over.bmp` *(was BMP/TGA)* |
| `btn_unbroken_pick.png` | 28×40 | `btn_unbroken_pick.bmp` *(was BMP/TGA)* |

`enchant_grade/extra/` — 12 additional components (not in ASSETS.md; from the concept sheet): `bg_main.png` 240×180, `bg_material.png` 176×56, `bg_result.png` 176×56, `bg_tab.png` 176×40, `btn_cancel.png` 72×30, `btn_enchant.png` 72×30, `btn_reset.png` 72×30, `grade_1.png` 40×26, `grade_2.png` 40×26, `grade_3.png` 40×26, `grade_4.png` 40×26, `grade_5.png` 40×26

### `equipment_doll/` — 5 drop-in replacements

| new file | size | replaces |
|---|---|---|
| `equipwin_bg.png` | 280×130 | `equipwin_bg.png` |
| `equipwin_bg2.png` | 280×157 | `equipwin_bg2.bmp` *(was BMP/TGA)* |
| `equipwin_bg2_change.png` | 280×179 | `equipwin_bg2_change.png` |
| `equipwin_special.png` | 280×133 | `equipwin_special.png` |
| `equipwin_special_change.png` | 280×179 | `equipwin_special_change.png` |

`equipment_doll/extra/` — 11 additional components (not in ASSETS.md; from the concept sheet): `bg_doll_preview.png` 116×96, `bg_slot.png` 44×44, `bg_slot_lock.png` 44×44, `bg_slot_on.png` 44×44, `bg_tab.png` 176×40, `slot_accessory.png` 44×44, `slot_body.png` 44×44, `slot_costume.png` 44×44, `slot_head.png` 44×44, `slot_shield.png` 44×44, `slot_weapon.png` 44×44

### `quest/` — 9 drop-in replacements

| new file | size | replaces |
|---|---|---|
| `bg_quest1.png` | 381×466 | `bg_quest1.png` |
| `bg_quest2.png` | 381×466 | `bg_quest2.png` |
| `bg_quest3.png` | 381×466 | `bg_quest3.png` |
| `bg_quest4.png` | 381×466 | `bg_quest4.png` |
| `bg_questlist.png` | 330×46 | `bg_questlist.png` |
| `bg_questsub.png` | 342×412 | `bg_questsub.png` |
| `img_poring.png` | 10×9 | `img_poring.png` |
| `img_questiocn.png` | 38×38 | `img_questiocn.bmp` *(was BMP/TGA)* |
| `quest_window.png` | 350×375 | `quest_window.bmp` *(was BMP/TGA)* |

`quest/extra/` — 10 additional components (not in ASSETS.md; from the concept sheet): `bg_detail.png` 176×64, `bg_list.png` 176×64, `bg_tab.png` 176×40, `btn_abandon.png` 72×30, `btn_navigate.png` 72×30, `icon_complete.png` 40×40, `icon_daily.png` 40×40, `icon_event.png` 40×40, `icon_main.png` 40×40, `icon_sub.png` 40×40

### `storage_tabs/` — 10 drop-in replacements

| new file | size | replaces |
|---|---|---|
| `tab_itm_01.png` | 20×82 | `tab_itm_01.bmp` *(was BMP/TGA)* |
| `tab_itm_02.png` | 20×82 | `tab_itm_02.bmp` *(was BMP/TGA)* |
| `tab_itm_03.png` | 20×82 | `tab_itm_03.bmp` *(was BMP/TGA)* |
| `tab_itm_ex_01.png` | 20×209 | `tab_itm_ex_01.png` |
| `tab_itm_ex_02.png` | 20×209 | `tab_itm_ex_02.png` |
| `tab_itm_ex_03.png` | 20×209 | `tab_itm_ex_03.png` |
| `tab_itm_ex_04.png` | 20×209 | `tab_itm_ex_04.png` |
| `tab_itm_ex_05.png` | 20×209 | `tab_itm_ex_05.png` |
| `tab_itm_ex_06.png` | 20×209 | `tab_itm_ex_06.png` |
| `tab_itm_ex_07.png` | 20×209 | `tab_itm_ex_07.png` |

`storage_tabs/extra/` — 10 additional components (not in ASSETS.md; from the concept sheet): `bg_slot.png` 40×40, `bg_slot_on.png` 40×40, `bg_tab.png` 176×40, `bg_window.png` 240×180, `btn_deposit.png` 44×34, `btn_lock.png` 44×34, `btn_search.png` 44×34, `btn_sort.png` 44×34, `btn_withdraw.png` 44×34, `slot_expand.png` 40×40

### `win_login/` — 1 drop-in replacements

| new file | size | replaces |
|---|---|---|
| `bg_login.png` | 301×132 | `bg_login.tga` *(was BMP/TGA)* |

`win_login/extra/` — 10 additional components (not in ASSETS.md; from the concept sheet): `bg_button.png` 132×26, `bg_input.png` 132×26, `bg_server_list.png` 132×40, `btn_exit.png` 44×30, `btn_login.png` 132×30, `btn_settings.png` 44×30, `checkbox.png` 20×20, `logo_top.png` 120×34, `server_status_off.png` 20×20, `server_status_on.png` 20×20