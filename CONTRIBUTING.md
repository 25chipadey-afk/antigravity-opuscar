# Contributing to Antigravity-Opuscar

Thanks for helping out. The easiest ways to contribute:

## Add a new style
1. Copy an existing folder in `styles/` (for example `styles/swiss-motion-graphics/`).
2. Edit `STYLE.md` (palette, typography, motion, sound) and `demo.html`.
3. Make sure `demo.html` implements `window.renderFrame(t, duration)` deterministically (see `TECHNIQUE.md`).
4. Preview it: `python tools/preview_frame.py --html styles/<id>/demo.html --time 2.0 --out preview.png`
5. Add a row for it to the styles table in `README.md`.

## Report a bug or suggest an idea
Open an issue with:
- your OS and Python version
- the command you ran
- the full error output

## Pull requests
- Keep changes focused. One style or fix per PR.
- Do not commit rendered films or `build/` folders (they are in `.gitignore`).
- Never commit API keys or `.env` files.

By contributing, you agree that your contributions are licensed under the MIT License.
