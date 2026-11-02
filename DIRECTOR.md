# 🎬 DIRECTOR.md — The Art of Code Filmmaking

You are directing a short film, not generating a slide deck. Every shot must have visual momentum, clear focal hierarchy, and tight synchronization between picture and sound.

---

## 1. Story Structure (The 4-Beat Micro-Arc)
Even a 30-second film needs a complete narrative arc:
1. **The Hook (0% – 20%)**: Open with immediate visual motion—never a static title card. Introduce the central tension, question, or anomaly in the first 3 seconds.
2. **The Mechanism / Journey (20% – 65%)**: Show *how* it works or *what* happened. Use progressive revelation: elements enter, interact, transform, or connect on screen in sync with the narrator's key nouns and verbs.
3. **The Climax / Shift (65% – 85%)**: Change the camera scale, color signal, or pacing. Zoom out to reveal the whole system, or zoom in to the decisive metric/moment.
4. **The Resolution & Echo (85% – 100%)**: Let the visual settle cleanly with a memorable closing motif and 1.0–1.5 seconds of breathing room after the last spoken word.

---

## 2. Visual Pacing & Motion Grammar
- **Never Freeze the Frame**: Even when text or a diagram is being read, keep subtle secondary motion alive (gentle camera drift, pulsing telemetry, floating dust/grain, or breathing strokes).
- **Easing Over Linear**: Never move objects with raw linear interpolation (`t`). Always apply easing curves (`easeOutCubic`, `easeInOutQuint`, or spring physics) so movements feel weighted and intentional.
- **One Idea Per Shot**: Each scene (`scene_01.html`, `scene_02.html`, ...) should last **4 to 8 seconds** and communicate one distinct visual beat. Avoid overcrowding more than 5 text labels on screen at once.

---

## 3. Typography & Layout Rules
- **Safe Margins**: Keep all critical text and focal graphics inside an **85% title-safe zone** (`140px` horizontal padding, `100px` vertical padding on a `1920x1080` canvas).
- **Contrast & Legibility**: Minimum font size on a 1080p canvas is `24px` for secondary annotations, `42px` for body statements, and `72px+` for hero headlines.
- **Kinetic Entrance**: Text should enter according to the style's grammar (e.g., masked slide-up for Swiss Motion, character-by-character decode for Cyber HUD, stroke-reveal for Chalkboard).

---

## 4. Narration & Sound Direction
- **Write for the Ear**: Keep sentences punchy (10–16 words per sentence). Use concrete numbers and vivid verbs instead of abstract filler.
- **Audio-Driven Timing**: In our pipeline, `core/voice_engine.py` synthesizes the narration for each scene first, measures its exact duration in seconds, and adds `0.8s` of tail padding. Your `window.renderFrame(t, duration)` function receives this exact `duration` so animations automatically scale to fit the spoken audio!

---

## 5. Self-Check Checklist Before Final Delivery
Before declaring a film complete, verify:
- [ ] Does every scene render without console errors or overlapping text?
- [ ] Are colors, fonts, and motion strictly faithful to `STYLE.md`?
- [ ] Does `core/verify.py` confirm valid resolution, 24 FPS frame rate, non-blank frames, and matched audio-video duration?
