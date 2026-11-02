#!/usr/bin/env python3
import argparse
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)

from core.render_engine import capture_single_frame

def main():
    parser = argparse.ArgumentParser(description="Render a preview PNG frame from an Opuscar scene HTML file.")
    parser.add_argument("--html", required=True, help="Path to scene HTML file")
    parser.add_argument("--time", type=float, default=2.5, help="Timestamp (seconds) to capture")
    parser.add_argument("--duration", type=float, default=6.0, help="Total scene duration")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--out", required=True, help="Output PNG path")
    args = parser.parse_args()

    out_path = capture_single_frame(
        html_path=args.html,
        out_png=args.out,
        time_sec=args.time,
        duration=args.duration,
        width=args.width,
        height=args.height
    )
    print(f"[preview_frame] Saved preview frame ({args.time}s) -> {out_path}")

if __name__ == "__main__":
    main()
