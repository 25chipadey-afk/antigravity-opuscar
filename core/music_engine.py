import math
import os
import struct
import wave

def synthesize_score(
    out_wav: str,
    duration: float,
    style: str = "cyber_pulse",
    sample_rate: int = 44100
) -> str:
    """
    Procedurally composes an original background score in pure Python (no external samples required).
    Supports styles: 'cyber_pulse', 'swiss_minimal', 'warm_ambient', 'chalk_focus'.
    """
    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)
    total_samples = int(math.ceil(duration * sample_rate))

    # Chord frequencies (A minor / C major9 cinematic palette)
    chords = [
        [220.0, 261.63, 329.63, 392.00],  # Am7
        [174.61, 220.00, 261.63, 349.23], # Fmaj7
        [130.81, 196.00, 246.94, 329.63], # Cmaj7
        [146.83, 220.00, 293.66, 349.23], # Dm7
    ]
    arp_notes = [220.0, 261.63, 329.63, 392.0, 440.0, 392.0, 329.63, 261.63]

    with wave.open(out_wav, "w") as wf:
        wf.setnchannels(2)  # Stereo
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)

        buf = bytearray()
        for i in range(total_samples):
            t = i / sample_rate
            # Global fade-in (1.0s) and fade-out (1.5s)
            fade_in = min(1.0, t / 1.0)
            fade_out = min(1.0, max(0.0, (duration - t) / 1.5))
            master_env = fade_in * fade_out

            chord_idx = int(t / 4.0) % len(chords)
            chord = chords[chord_idx]

            left = 0.0
            right = 0.0

            if style == "cyber_pulse":
                # Deep sub-bass pulse + 8th-note digital arpeggio
                bass_freq = chord[0] * 0.5
                beat_phase = (t * 2.0) % 1.0
                bass_env = math.exp(-beat_phase * 4.5)
                bass = math.sin(2 * math.pi * bass_freq * t) * bass_env * 0.45

                step = int(t * 4.0) % len(arp_notes)
                note_phase = (t * 4.0) % 1.0
                pluck_env = math.exp(-note_phase * 7.0)
                arp_freq = arp_notes[step]
                pluck = (
                    math.sin(2 * math.pi * arp_freq * t) * 0.6 +
                    math.sin(2 * math.pi * arp_freq * 2.0 * t) * 0.25
                ) * pluck_env * 0.25

                pad = sum(math.sin(2 * math.pi * f * t) for f in chord) * 0.06
                left = bass + pad + pluck * 0.9
                right = bass + pad + pluck * 1.1

            elif style == "swiss_minimal":
                # Crisp metronomic tick + warm harmonic triad on beats
                beat_phase = (t * 2.0) % 1.0
                click_env = math.exp(-beat_phase * 40.0)
                click = math.sin(2 * math.pi * 1200.0 * t) * click_env * 0.15

                chord_env = math.exp(-((t * 0.5) % 1.0) * 2.2)
                pad = sum(math.sin(2 * math.pi * f * t) for f in chord) * chord_env * 0.14
                left = pad + click
                right = pad + click * 0.8

            elif style == "chalk_focus":
                # Gentle marimba-like harmonic plucks
                step = int(t * 2.5) % len(arp_notes)
                note_phase = (t * 2.5) % 1.0
                marimba_env = math.exp(-note_phase * 6.0)
                freq = arp_notes[step]
                marimba = (
                    math.sin(2 * math.pi * freq * t) +
                    0.2 * math.sin(2 * math.pi * freq * 4.0 * t) * math.exp(-note_phase * 18.0)
                ) * marimba_env * 0.28
                warm_pad = math.sin(2 * math.pi * chord[0] * t) * 0.12
                left = warm_pad + marimba
                right = warm_pad + marimba * 0.95

            else:  # "warm_ambient" default
                # Slow-breathing lush sine/triangle pad
                lfo = 0.75 + 0.25 * math.sin(2 * math.pi * 0.2 * t)
                for idx, f in enumerate(chord):
                    voice_wave = math.sin(2 * math.pi * f * t + idx * 0.4) * 0.12 * lfo
                    left += voice_wave * (0.8 + 0.1 * idx)
                    right += voice_wave * (1.1 - 0.1 * idx)

            s_left = max(-32767, min(32767, int(left * master_env * 32767)))
            s_right = max(-32767, min(32767, int(right * master_env * 32767)))
            buf.extend(struct.pack("<hh", s_left, s_right))

        wf.writeframes(bytes(buf))
    return out_wav
