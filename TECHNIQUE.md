# ⚙️ TECHNIQUE.md — Deterministic Rendering & Pipeline Guide

To render silky-smooth 24 FPS video from HTML5 Canvas, SVG, and WebGL without dropped frames, every scene file MUST obey the **Deterministic Time Contract**.

---

## 1. The Mandatory HTML Scene Contract

Every scene (`films/<slug>/scenes/scene_XX.html`) is loaded into Headless Chromium at `1920x1080` (or `1080x1920`). The Python renderer (`core/render_engine.py`) steps through time frame-by-frame (`frame = 0, 1, 2, ...`) and calls:

```javascript
window.renderFrame(t, duration);
```

Where:
- `t` (float): Current scene time in seconds (`frame / fps`, starting at `0.0`).
- `duration` (float): Total duration of this scene in seconds (automatically determined by the voiceover length + padding, or specified in `project.json`).
- Normalized progress is simply `const p = Math.min(1, Math.max(0, t / duration));`.

### Browser Preview Fallback
So you (or the user) can also open any `scene_XX.html` directly in a normal browser to watch it play in real time, include this snippet at the bottom of your script:

```javascript
// Auto-play in regular browser if not controlled by headless renderer
if (!navigator.webdriver && !window.__OPUSCAR_HEADLESS__) {
  const defaultDuration = 6.0;
  const start = performance.now();
  function loop(now) {
    const t = ((now - start) / 1000) % defaultDuration;
    window.renderFrame(t, defaultDuration);
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
}
```

---

## 2. Determinism Rules (No Flicker!)

1. **Never use `Math.random()` inside `renderFrame(t)`**:
   Calling `Math.random()` on every frame causes particles, stars, or brushstroke jitter to explode into chaotic noise. Instead, use a seeded pseudo-random generator initialized once or indexed by particle ID:
   ```javascript
   function seededRandom(seed) {
     let x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
     return x - Math.floor(x);
   }
   ```
2. **Never rely on `setInterval`, `setTimeout`, or CSS `@keyframes`**:
   Headless frame capture may render faster or slower than real-time wall-clock speed. Compute **all** positions, opacities, camera angles, and SVG stroke offsets purely as a mathematical function of `t` and `duration`.

---

## 3. Standard Easing & Clamping Helpers

Include these utility functions in your scenes for cinema-grade motion:

```javascript
const clamp = (v, min = 0, max = 1) => Math.min(max, Math.max(min, v));
const remap = (t, t0, t1) => clamp((t - t0) / (t1 - t0), 0, 1);
const lerp = (a, b, p) => a + (b - a) * clamp(p);

const Easing = {
  outCubic: (x) => 1 - Math.pow(1 - clamp(x), 3),
  inOutCubic: (x) => {
    x = clamp(x);
    return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  },
  outQuint: (x) => 1 - Math.pow(1 - clamp(x), 5),
  outBack: (x) => {
    x = clamp(x);
    const c1 = 1.70158, c3 = c1 + 1;
    return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
  }
};
```

---

## 4. Project Manifest (`films/<slug>/project.json`)

Each film is defined by a clean JSON manifest:

```json
{
  "title": "How TCP 3-Way Handshake Works",
  "slug": "demo-tcp-handshake",
  "style": "cyber-network-hud",
  "width": 1920,
  "height": 1080,
  "fps": 24,
  "voice": "en-US-ChristopherNeural",
  "music_style": "cyber_pulse",
  "music_volume": 0.18,
  "scenes": [
    {
      "id": "scene_01",
      "html": "scenes/scene_01.html",
      "narration": "Before two computers can exchange a single byte of data over TCP, they must agree to talk.",
      "min_duration": 5.0,
      "tail_padding": 0.8
    }
  ]
}
```

### Supported `music_style` Presets (`core/music_engine.py`):
- `"cyber_pulse"` — Deep sub-bass pulse with arpeggiated digital plucks.
- `"swiss_minimal"` — Crisp percussive clicks and warm sine/triangle harmonic chords on the beat.
- `"warm_ambient"` — Lush, slow-attack acoustic-style pads for watercolor/documentary films.
- `"chalk_focus"` — Gentle marimba/kalimba-like harmonic notes for educational explainers.
