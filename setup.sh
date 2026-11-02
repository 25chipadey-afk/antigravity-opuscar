#!/usr/bin/env bash
set -e
echo "🎬 Setting up Antigravity-Opuscar environment..."
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
if command -v ffmpeg >/dev/null 2>&1; then
  echo "✅ FFmpeg detected: $(ffmpeg -version | head -n 1)"
else
  echo "⚠️  FFmpeg not found in PATH! Please install FFmpeg (e.g., sudo apt install ffmpeg or brew install ffmpeg)."
fi
echo "✅ Setup complete! Open this folder in Antigravity IDE and run /make-film."
