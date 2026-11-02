---
description: Create a complete code-rendered short film in Antigravity-Opuscar
---

1. Ask the user (if not already specified):
   - Topic / story of the film
   - Preferred style from `styles/` (or `my-styles/`)
   - Target duration (default: 30 seconds) and aspect ratio (`1920x1080` landscape or `1080x1920` vertical)
2. Read `DIRECTOR.md`, `TECHNIQUE.md`, and `styles/<selected-style>/STYLE.md`.
3. Run `python tools/init_project.py --slug <slug> --style <selected-style> --title "<Title>"`.
4. Populate `films/<slug>/project.json` with a multi-scene storyboard, voiceover script, and music mood.
5. Create deterministic HTML scene files in `films/<slug>/scenes/scene_XX.html` implementing `window.renderFrame(t, duration)`.
6. Render a mid-scene preview frame using `python tools/preview_frame.py` to verify layout and typography.
7. Build the complete MP4 video using `python tools/build_film.py --project films/<slug>/project.json`.
