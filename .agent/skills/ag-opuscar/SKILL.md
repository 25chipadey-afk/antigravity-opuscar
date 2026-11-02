---
name: ag-opuscar
description: Direct and render short animated films in 2D Canvas, SVG, and 3D WebGL/Three.js entirely in code with TTS voiceover and procedural music.
---

# Skill: Antigravity-Opuscar (`ag-opuscar`)

## When to Use
Use this skill when the user wants to:
- Create an animated short film, explainer video, or motion-graphics piece from a prompt.
- Browse or preview the visual styles in `styles/`.
- Customize an existing visual style or design a brand-new visual style (`MY-STYLES.md`).

## Execution Steps
1. Read `DIRECTOR.md` and `TECHNIQUE.md`.
2. Select the matching style from `styles/<style-id>/STYLE.md` (or `my-styles/<style-id>/STYLE.md`).
3. Scaffold the film workspace with `python tools/init_project.py`.
4. Write `films/<slug>/project.json` and the deterministic HTML scene files inside `films/<slug>/scenes/`.
5. Execute `python tools/build_film.py --project films/<slug>/project.json` and report the generated `.mp4` path to the user.
