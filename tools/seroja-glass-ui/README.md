# SeROja Glass UI — asset generators

Every PNG in `assets/seroja-glass-ui/` is generated from this code, so the whole
skin can be re-rendered after a palette or radius change instead of being
re-drawn by hand.

## Run

```sh
pip install Pillow numpy
cd tools/seroja-glass-ui
OUT=../../assets/seroja-glass-ui python3 s1_achievement.py
OUT=../../assets/seroja-glass-ui python3 s2_cashshop.py
# ... s3 .. s8, then:
OUT=../../assets/seroja-glass-ui python3 extras.py
```

Each section script asserts its own output dimensions and fails loudly if a
canvas drifts, because the client positions everything on top of these by
hardcoded pixel offsets.

## Layout

- `glass.py` — the drawing primitives: palette tokens, supersampled rounded-rect
  and ring masks, `glass_panel()`, `button()`, `slot()`, `inset_well()`,
  `titlebar()`, text and compositing helpers. Everything renders at 4× and
  LANCZOS-downsamples so 1px hairlines stay clean.
- `icons.py` — the glyph vocabulary. Each icon is authored in a 0..1 unit box and
  scaled by the caller, so the same sword reads at 13px on a storage tab and at
  40px on a button.
- `s1..s8_*.py` — one script per window; each holds the geometry measured off the
  original bitmaps.
- `extras.py` — the additional components from the concept sheet.
- `preview.py` — contact sheets for eyeballing a section.

Palette values mirror `src/UI/Components/SeROjaCommon/glassTheme.css`; change them
in `glass.py` and re-run to restyle the whole set.
