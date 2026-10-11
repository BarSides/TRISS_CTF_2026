#!/usr/bin/env python3
"""Generate files/voicemail.wav for the Scatter Shot challenge.

Organizer only: do not attach this script or solve.py in CTFd. It
synthesises a short chime tune (standard library only), then hides the flag
with the same files/scatter.py that players receive.
"""
import importlib.util
import math
import random
import struct
import sys
import tempfile
import wave
from pathlib import Path

FLAG = "BarSides{four_digits_is_not_a_key}"
PIN = 412                     # "0412", Pittsburgh's area code
RATE = 22050
HERE = Path(__file__).resolve().parent
FILES = HERE.parent / "files"

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("scatter", FILES / "scatter.py")
scatter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scatter)

# An original little tune: (note, beats). Note numbers are semitones from A4.
TUNE = [(3, 1), (7, 1), (10, 1), (15, 2), (14, 1), (10, 1), (12, 2), (7, 2),
        (8, 1), (12, 1), (15, 1), (19, 2), (17, 1), (15, 1), (14, 4),
        (3, 1), (7, 1), (10, 1), (15, 2), (17, 1), (19, 1), (22, 2), (15, 2),
        (14, 1), (12, 1), (10, 1), (7, 1), (8, 2), (10, 2), (3, 4)]
BEAT = 0.3


def synth():
    rng = random.Random(1022)
    samples = [0.0] * int(RATE * 0.4)               # a breath of silence
    for note, beats in TUNE:
        f = 440 * 2 ** (note / 12)
        n = int(RATE * BEAT * beats)
        for t in range(n):
            s = t / RATE
            env = min(1, t / 200) * math.exp(-3.2 * s)
            v = (math.sin(2 * math.pi * f * s) + 0.35 * math.sin(4 * math.pi * f * s)
                 + 0.12 * math.sin(6 * math.pi * f * s))
            samples.append(0.28 * env * v)
    samples += [0.0] * int(RATE * 0.8)
    # Light tape hiss so the low bits look random everywhere, not only
    # where the message landed.
    return [max(-32768, min(32767, int(v * 32767) + rng.randint(-6, 6))) for v in samples]


def main():
    pcm = synth()
    with tempfile.TemporaryDirectory() as tmp:
        cover = Path(tmp) / "cover.wav"
        with wave.open(str(cover), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes(struct.pack(f"<{len(pcm)}h", *pcm))
        scatter.hide(str(cover), str(FILES / "voicemail.wav"), FLAG, PIN)
    print(f"wrote {FILES / 'voicemail.wav'} ({len(pcm) / RATE:.1f}s)")


if __name__ == "__main__":
    main()
