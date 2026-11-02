import os
import subprocess
from typing import List

def mux_scene_audio_video(video_mp4: str, voice_wav: str, out_mp4: str, total_duration: float) -> str:
    """Pads the scene voiceover WAV to match the scene video duration and merges them."""
    os.makedirs(os.path.dirname(os.path.abspath(out_mp4)), exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-i", video_mp4,
        "-i", voice_wav,
        "-filter_complex", f"[1:a]apad=whole_dur={total_duration:.4f}[aout]",
        "-map", "0:v:0",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out_mp4
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return out_mp4

def assemble_final_film(
    scene_mp4s: List[str],
    music_wav: str,
    out_mp4: str,
    music_volume: float = 0.18
) -> str:
    """
    Concatenates all scene clips and mixes the procedural music score underneath the narration
    with broadcast loudness normalization.
    """
    abs_out = os.path.abspath(out_mp4)
    work_dir = os.path.dirname(abs_out)
    concat_list_path = os.path.join(work_dir, "concat_list.txt")
    concat_temp_mp4 = os.path.join(work_dir, "_concat_raw.mp4")

    with open(concat_list_path, "w", encoding="utf-8") as f:
        for clip in scene_mp4s:
            safe_path = os.path.abspath(clip).replace("\\", "/")
            f.write(f"file '{safe_path}'\n")

    # Step 1: Concatenate scene clips
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        concat_temp_mp4
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)

    # Step 2: Mix narration track [0:a] with background score [1:a]
    filter_complex = (
        f"[0:a]volume=1.0[voice];"
        f"[1:a]volume={music_volume:.3f}[bgm];"
        f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[mixed]"
    )
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", concat_temp_mp4,
        "-i", music_wav,
        "-filter_complex", filter_complex,
        "-map", "0:v:0",
        "-map", "[mixed]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        abs_out
    ]
    subprocess.run(cmd_mix, capture_output=True, check=True)

    if os.path.exists(concat_temp_mp4):
        os.remove(concat_temp_mp4)
    return abs_out
