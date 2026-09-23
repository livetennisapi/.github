# Profile artwork

The hero has wide and phone layouts. Both SVGs follow the viewer's light or dark theme.
Lettering uses Geist outlines, so no font request is needed. The font license is in [Geist-OFL.txt](Geist-OFL.txt).

Regenerate the artwork with Python, `fonttools[woff]` and a local Geist variable font.
Set `GEIST_FONT` to the font's path, then run this from the repository root.

```bash
python3 scripts/render-profile-art.py --font "$GEIST_FONT"
```

The artwork has no scripts, animation or external assets.
