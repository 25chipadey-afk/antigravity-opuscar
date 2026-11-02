#!/usr/bin/env python3
import argparse
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)

from core.voice_engine import synthesize_narration
from core.music_engine import synthesize_score
from core.render_engine import render_scene_to_mp4
from core.mixer import mux_scene_audio_video, assemble_final_film
from core.verify import verify_mp4

def main():
    parser = argparse.ArgumentParser(description="Build a complete MP4 film from an Antigravity-Opuscar project.json")
    parser.add_argument("--project", required=True, help="Path to project.json")
    args = parser.parse_args()

    project_path = os.path.abspath(args.project)
    project_dir = os.path.dirname(project_path)
    build_dir = os.path.join(project_dir, "build")
    os.makedirs(build_dir, exist_ok=True)

    with open(project_path, "r", encoding="utf-8") as f:
        project = json.load(f)

    title = project.get("title", "Film")
    slug = project.get("slug", "output")
    width = int(project.get("width", 1920))
    height = int(project.get("height", 1080))
    fps = int(project.get("fps", 24))
    voice = project.get("voice", "en-US-ChristopherNeural")
    music_style = project.get("music_style", "cyber_pulse")
    music_volume = float(project.get("music_volume", 0.18))
    scenes = project.get("scenes", [])

    print(f"==================================================")
    print(f"🎬 Building Antigravity-Opuscar Film: {title}")
    print(f"   Resolution: {width}x{height} @ {fps}fps | Scenes: {len(scenes)}")
    print(f"==================================================")

    muxed_scene_clips = []
    total_film_duration = 0.0

    for idx, scene in enumerate(scenes, start=1):
        scene_id = scene.get("id", f"scene_{idx:02d}")
        rel_html = scene["html"]
        html_path = os.path.join(project_dir, rel_html)
        narration = scene.get("narration", "")
        min_dur = float(scene.get("min_duration", 4.5))
        tail_pad = float(scene.get("tail_padding", 0.8))

        print(f"\n[{idx}/{len(scenes)}] Scene '{scene_id}':")
        voice_wav = os.path.join(build_dir, f"{scene_id}_voice.wav")
        voice_dur = synthesize_narration(narration, voice_wav, voice=voice)
        scene_duration = max(min_dur, round(voice_dur + tail_pad, 2))
        total_film_duration += scene_duration
        print(f"  🎙️ Narration ({voice_dur:.2f}s) -> Scene duration locked at {scene_duration:.2f}s")

        raw_video_mp4 = os.path.join(build_dir, f"{scene_id}_video.mp4")
        print(f"  🎨 Rendering {int(round(scene_duration * fps))} frames from {rel_html} ...")
        render_scene_to_mp4(
            html_path=html_path,
            out_mp4=raw_video_mp4,
            duration=scene_duration,
            width=width,
            height=height,
            fps=fps
        )

        scene_final_mp4 = os.path.join(build_dir, f"{scene_id}_muxed.mp4")
        mux_scene_audio_video(raw_video_mp4, voice_wav, scene_final_mp4, scene_duration)
        muxed_scene_clips.append(scene_final_mp4)

    print(f"\n🎵 Synthesizing '{music_style}' background score ({total_film_duration:.2f}s) ...")
    music_wav = os.path.join(build_dir, "score.wav")
    synthesize_score(music_wav, duration=total_film_duration + 1.0, style=music_style)

    final_mp4 = os.path.join(project_dir, f"{slug}.mp4")
    print(f"🎞️ Mixing final film -> {final_mp4}")
    assemble_final_film(muxed_scene_clips, music_wav, final_mp4, music_volume=music_volume)

    report = verify_mp4(final_mp4, expected_width=width, expected_height=height)
    print(f"\n✅ Verification Report: {json.dumps(report, indent=2)}")
    if not report.get("ok"):
        sys.exit(1)

if __name__ == "__main__":
    main()
