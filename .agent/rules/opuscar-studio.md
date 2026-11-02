---
trigger: always_on
description: Antigravity-Opuscar Code-Based Filmmaking Studio Rules
---

# Opuscar Studio Rule for Antigravity

Whenever the user asks to create a film, animation, explainer video, or custom visual style:
1. Check `AGENTS.md`, `DIRECTOR.md`, and `TECHNIQUE.md`.
2. Browse available styles in `styles/` (or user-saved styles in `my-styles/`).
3. Ensure every HTML scene implements `window.renderFrame(t, duration)` deterministically.
4. Use `tools/build_film.py` to compile the final `.mp4` video and `core/verify.py` to verify output integrity.
