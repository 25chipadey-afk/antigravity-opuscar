@echo off
echo Setting up Antigravity-Opuscar environment...
pip install -r requirements.txt
playwright install chromium
where ffmpeg >nul 2>nul
if %errorlevel%==0 (
    echo FFmpeg detected!
) else (
    echo WARNING: FFmpeg not found in PATH! Please install FFmpeg: winget install Gyan.FFmpeg
)
echo Setup complete! Open this folder in Antigravity IDE and run /make-film.
