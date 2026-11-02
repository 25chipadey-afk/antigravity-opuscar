import asyncio
import math
import os
import struct
import subprocess
import wave

def get_wav_duration(wav_path: str) -> float:
    with wave.open(wav_path, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)

def get_media_duration(media_path: str) -> float:
    """Uses ffprobe to measure exact audio duration in seconds."""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            media_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        if media_path.endswith(".wav") and os.path.exists(media_path):
            return get_wav_duration(media_path)
        return 5.0

def generate_fallback_speech_wav(text: str, out_wav: str, sample_rate: int = 44100) -> float:
    """
    Offline fallback: Generates a pleasant, soft UI-style cadence & silence track
    timed to the word count (~2.6 words/sec) if edge-tts / internet is unavailable.
    """
    words = text.strip().split()
    duration = max(3.0, len(words) / 2.6 + 0.6)
    total_samples = int(duration * sample_rate)
    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)

    with wave.open(out_wav, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        buf = bytearray()
        for i in range(total_samples):
            t = i / sample_rate
            # Subtle soft syllable-like envelope chime at start of scene
            env = math.exp(-t * 4.0) if t < 0.8 else 0.0
            val = math.sin(2 * math.pi * 320.0 * t) * env * 0.08
            sample = max(-32767, min(32767, int(val * 32767)))
            buf.extend(struct.pack("<h", sample))
        wf.writeframes(bytes(buf))
    return duration

async def _edge_tts_synthesize(text: str, voice: str, out_mp3: str):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_mp3)

def synthesize_narration(text: str, out_wav: str, voice: str = "en-US-ChristopherNeural") -> float:
    """
    Synthesizes voiceover narration for a scene and outputs a standard 44.1kHz mono WAV.
    Returns exact audio duration in seconds.
    """
    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)
    if not text or not text.strip():
        return generate_fallback_speech_wav("...", out_wav)

    temp_mp3 = out_wav.replace(".wav", "_raw.mp3")
    try:
        asyncio.run(_edge_tts_synthesize(text, voice, temp_mp3))
        # Convert MP3 to normalized 44.1kHz WAV via FFmpeg
        cmd = [
            "ffmpeg", "-y", "-i", temp_mp3,
            "-ar", "44100", "-ac", "1",
            out_wav
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
        return get_media_duration(out_wav)
    except Exception as e:
        print(f"[voice_engine] edge-tts unavailable ({e}), using timed cadence fallback.")
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
        return generate_fallback_speech_wav(text, out_wav)
