import os
import subprocess
from playwright.sync_api import sync_playwright

def render_scene_to_mp4(
    html_path: str,
    out_mp4: str,
    duration: float,
    width: int = 1920,
    height: int = 1080,
    fps: int = 24
) -> str:
    """
    Renders a single deterministic HTML scene (`window.renderFrame(t, duration)`)
    frame-by-frame in headless Chromium and pipes raw PNG frames directly to FFmpeg
    to create a pristine H.264 `.mp4` video clip.
    """
    abs_html = os.path.abspath(html_path)
    abs_out = os.path.abspath(out_mp4)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)
    total_frames = max(1, int(round(duration * fps)))

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "image2pipe",
        "-vcodec", "png",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "18",
        abs_out
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        page.add_init_script("window.__OPUSCAR_HEADLESS__ = true;")
        page.goto(f"file://{abs_html}", wait_until="load")

        for frame_idx in range(total_frames):
            t = frame_idx / float(fps)
            page.evaluate(f"if (window.renderFrame) {{ window.renderFrame({t:.6f}, {duration:.6f}); }}")
            png_bytes = page.screenshot(type="png")
            proc.stdin.write(png_bytes)

        browser.close()

    proc.stdin.close()
    stderr_out = proc.stderr.read().decode("utf-8", errors="replace")
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg scene encoding failed:\n{stderr_out}")

    return abs_out

def capture_single_frame(
    html_path: str,
    out_png: str,
    time_sec: float = 2.0,
    duration: float = 6.0,
    width: int = 1920,
    height: int = 1080
) -> str:
    """Captures a single preview frame at `time_sec` for storyboard/style inspection."""
    abs_html = os.path.abspath(html_path)
    abs_out = os.path.abspath(out_png)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        page.add_init_script("window.__OPUSCAR_HEADLESS__ = true;")
        page.goto(f"file://{abs_html}", wait_until="load")
        page.evaluate(f"if (window.renderFrame) {{ window.renderFrame({time_sec:.6f}, {duration:.6f}); }}")
        page.screenshot(path=abs_out, type="png")
        browser.close()

    return abs_out
