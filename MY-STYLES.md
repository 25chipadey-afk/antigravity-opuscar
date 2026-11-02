# 🎨 MY-STYLES.md — Make a Style Your Own

Every creator or channel has its own visual signature: brand colors, typography, recurring motifs, or camera feel. Follow this **5-Step Protocol** whenever the user wants to customize a library style or design a new style from scratch.

---

## Two Ways In
1. **Modify a Library Style**: Pick one of the existing styles in `styles/<style-id>/` as the technical foundation and alter its palette, materials, typography, or pace.
2. **Start from a Blank Page**: The user describes a look (e.g., *"Blueprint architectural drafting with glowing cyan lines"*). Pick the closest library style as the rendering scaffold and transform it.

---

## The 5-Step Style Creation Workflow

### Step 1: Plan It (Sort into 3 Buckets)
Present a quick breakdown to the user before writing code:
- **Safe to Change**: Color palette, font stack, pacing/speed, aspect ratio (`1920x1080` vs `1080x1920`), sound mood.
- **Changes Character**: Surface texture (flat vs paper grain vs CRT scanlines), lighting/shadows, camera grammar (static grid vs isometric orbit).
- **Core Essence (Keep)**: Deterministic `window.renderFrame(t, duration)` loop and clean visual hierarchy.

### Step 2: Review the Summary
Show a concise Before → After table of the style attributes. Wait for user confirmation (or proceed immediately if the user says *"you decide"*).

### Step 3: Render a Single Style Frame (`preview_frame.py`)
Create `my-styles/<style-slug>/STYLE.md` and `my-styles/<style-slug>/demo.html`.
Render a test frame at `t = 2.5s`:
```bash
python tools/preview_frame.py --html my-styles/<style-slug>/demo.html --time 2.5 --out my-styles/<style-slug>/preview.png
```
If modifying a library style, you can also render a side-by-side comparison frame using `--compare styles/<base-style>/demo.html`.

### Step 4: Render a 10-Second Demo Film
Once the still frame looks great, build a short 2-scene demo film showcasing the style's entrance animations, typography, and custom music mood.

### Step 5: Save to `my-styles/<style-slug>/`
Keep the finalized `STYLE.md`, `demo.html`, and `preview.png` inside `my-styles/<style-slug>/`. From now on, the user can request any film in their custom style by name!
