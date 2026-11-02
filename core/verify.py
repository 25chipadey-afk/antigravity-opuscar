import json
import os
import subprocess
from typing import Dict, Any

def verify_mp4(mp4_path: str, expected_width: int = 1920, expected_height: int = 1080) -> Dict[str, Any]:
    """
    Runs automated self-checks on the rendered MP4 file (streams, resolution, duration, file size).
    """
    if not os.path.exists(mp4_path):
        return {"ok": False, "error": f"File not found: {mp4_path}"}

    file_size = os.path.getsize(mp4_path)
    if file_size < 1024:
        return {"ok": False, "error": f"File too small ({file_size} bytes)"}

    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
            "-of", "json",
            mp4_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(res.stdout)
        streams = info.get("streams", [])
        video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
        duration = float(info.get("format", {}).get("duration", 0.0))

        if not video_stream:
            return {"ok": False, "error": "Missing video stream"}
        if not audio_stream:
            return {"ok": False, "error": "Missing audio stream"}

        w = int(video_stream.get("width", 0))
        h = int(video_stream.get("height", 0))
        if w != expected_width or h != expected_height:
            return {"ok": False, "error": f"Resolution mismatch: got {w}x{h}, expected {expected_width}x{expected_height}"}

        return {
            "ok": True,
            "path": mp4_path,
            "width": w,
            "height": h,
            "duration_sec": round(duration, 2),
            "size_kb": round(file_size / 1024.0, 1)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
