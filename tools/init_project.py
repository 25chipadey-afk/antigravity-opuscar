#!/usr/bin/env python3
import argparse
import json
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description="Initialize a new Antigravity-Opuscar film project.")
    parser.add_argument("--slug", required=True, help="Project folder slug (e.g. dns-explained)")
    parser.add_argument("--style", default="swiss-motion-graphics", help="Style ID from styles/ or my-styles/")
    parser.add_argument("--title", default="Untitled Film", help="Film title")
    parser.add_argument("--vertical", action="store_true", help="Use vertical 1080x1920 resolution")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    film_dir = os.path.join(repo_root, "films", args.slug)
    scenes_dir = os.path.join(film_dir, "scenes")
    os.makedirs(scenes_dir, exist_ok=True)

    # Check if style demo exists to copy as starter template
    style_demo = os.path.join(repo_root, "styles", args.style, "demo.html")
    if not os.path.exists(style_demo):
        style_demo = os.path.join(repo_root, "my-styles", args.style, "demo.html")

    scene_01_path = os.path.join(scenes_dir, "scene_01.html")
    if os.path.exists(style_demo) and not os.path.exists(scene_01_path):
        shutil.copyfile(style_demo, scene_01_path)

    style_to_music = {
        "swiss-motion-graphics": "swiss_minimal",
        "cyber-network-hud": "cyber_pulse",
        "watercolor-storybook": "warm_ambient",
        "isometric-3d-diorama": "swiss_minimal",
        "evidence-documentary": "warm_ambient",
        "chalkboard-lecture": "chalk_focus"
    }

    manifest = {
        "title": args.title,
        "slug": args.slug,
        "style": args.style,
        "width": 1080 if args.vertical else 1920,
        "height": 1920 if args.vertical else 1080,
        "fps": 24,
        "voice": "en-US-ChristopherNeural",
        "music_style": style_to_music.get(args.style, "warm_ambient"),
        "music_volume": 0.18,
        "scenes": [
            {
                "id": "scene_01",
                "html": "scenes/scene_01.html",
                "narration": f"{args.title}. Directed and rendered in code.",
                "min_duration": 5.0,
                "tail_padding": 0.8
            }
        ]
    }

    manifest_path = os.path.join(film_dir, "project.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[init_project] Initialized film project at: {film_dir}")
    print(f"[init_project] Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
