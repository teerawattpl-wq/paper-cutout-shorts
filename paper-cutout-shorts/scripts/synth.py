"""Shared sound building blocks: synthesized effects, a storybook music loop, and voice-line helpers."""
import os, wave
import numpy as np
from scipy.signal import resample_poly, lfilter, butter

SR = 44100
rng = np.random.default_rng(7)


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(d, a=0.005, k=6.0):
    t = tt(d)
    return np.minimum(t / a, 1) * np.exp(-k * t / d)


def filt(x, lo=None, hi=None):
    if lo and hi:
        b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band")
    elif lo:
        b, a = butter(2, lo / (SR / 2), "high")
    else:
        b, a = butter(2, hi / (SR / 2), "low")
    return lfilter(b, a, x)


def noise(d):
    return rng.standard_normal(int(d * SR))


def sweep(f0, f1, d):
    return np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, int(d * SR))) / SR)


def pop():
    return sweep(380, 950, 0.07) * env(0.07, k=4)


def tap():
    return filt(noise(0.03), lo=1800) * env(0.03, 0.001, 7)


def thud(big=False):
    d = 0.45 if big else 0.22
    return sweep(110, 42, d) * env(d, k=5) + 0.35 * filt(noise(d), hi=400) * env(d, k=9)


def boing():
    d = 0.38
    t = tt(d)
    f = 210 + 190 * t / d + 28 * np.sin(2 * np.pi * 22 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, k=3.5)


def swish(d=0.28, lo=900, hi=5000):
    return filt(noise(d), lo=lo, hi=hi) * np.sin(np.pi * tt(d) / d) ** 2


def rustle():
    return filt(noise(0.4), lo=2500) * env(0.4, 0.03, 4) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 23 * tt(0.4))))


def whistle(d=1.5, f0=700, f1=2100):
    t = tt(d)
    x = sweep(f0, f1, d) * (1 + 0.25 * np.sin(2 * np.pi * 9 * t))
    return x * np.minimum(t / 0.03, 1) * np.exp(-2.6 * t / d)


def bell(f, d=0.9):
    t = tt(d)
    x = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-6 * t) + 0.2 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-12 * t)
    return x * np.minimum(t / 0.002, 1) * np.exp(-4.5 * t)


def sparkle():
    x = np.zeros(int(0.9 * SR))
    for i, f in enumerate([1568, 2093, 2637, 3136]):
        b = bell(f, 0.5)
        j = int(i * 0.07 * SR)
        x[j:j + len(b)] += b * 0.5
    return x


def snore():
    """One breath: a rumbling inhale, then a soft whistling exhale."""
    d1, d2 = 1.0, 0.9
    t1 = tt(d1)
    inhale = filt(noise(d1), lo=60, hi=320) * np.sin(np.pi * t1 / d1) ** 1.5 * (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 27 * t1)))
    t2 = tt(d2)
    exhale = (0.5 * sweep(880, 640, d2) + 0.25 * filt(noise(d2), lo=2000, hi=6000)) * np.sin(np.pi * t2 / d2) ** 2
    return np.concatenate([inhale * 1.6, np.zeros(int(0.12 * SR)), exhale * 0.35])


def pluck(f, d=0.5, bright=1.0):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * f * h * t) * np.exp(-(5 + 3.5 * h) * t) / h ** (1.6 / bright) for h in range(1, 7))
    return x * np.minimum(t / 0.003, 1)


def rms(x):
    return np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2))


def put(buf, t, x, gain=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    x = x[: len(buf) - i]
    buf[i:i + len(x)] += x * gain


def load_line(path, start=0.0, end=None):
    w = wave.open(path)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    x = x[int(start * w.getframerate()): int(end * w.getframerate()) if end else None]
    x = resample_poly(x, SR, w.getframerate())
    return x / (np.abs(x).max() + 1e-9) * 0.7


def far(x, gain=0.75, hi=3200, echoes=((0.11, 0.28), (0.23, 0.14))):
    """Make a voice sound distant: thinner, quieter, with a small echo."""
    y = filt(x, lo=350, hi=hi) * gain
    out = np.zeros(len(y) + int(0.6 * SR))
    out[:len(y)] += y
    for dly, g in echoes:
        j = int(dly * SR)
        out[j:j + len(y)] += y * g
    return out


NOTE = {"C": 261.63, "D": 293.66, "E": 329.63, "F": 349.23, "G": 392.0, "A": 440.0, "B": 493.88}
BARS = [
    ("C2", ["E4", "G4", "C5"], ["E5", "G5", None, "C6"]),
    ("A2", ["E4", "A4", "C5"], ["A5", None, "E5", None]),
    ("F2", ["F4", "A4", "C5"], ["F5", "A5", None, "C6"]),
    ("G2", ["D4", "G4", "B4"], ["D5", None, "G5", "B5"]),
]


def hz(name):
    return NOTE[name[0]] * 2 ** (int(name[1]) - 4)


def music_loop(dur, beat=0.6):
    """Plucked bass, ukulele-style chords and glockenspiel, about 100 BPM."""
    buf = np.zeros(int(dur * SR))
    t, bar = 0.0, 0
    while t < dur:
        bass, chord, mel = BARS[bar % 4]
        for b in range(4):
            bt = t + b * beat
            if b in (0, 2):
                put(buf, bt, pluck(hz(bass) * 2, 0.55, 0.8), 0.9)
            for i, c in enumerate(chord):
                put(buf, bt + beat / 2 + i * 0.012, pluck(hz(c), 0.4, 1.3), 0.32)
            if mel[b] and (bar % 2 == 0 or b == 0):
                put(buf, bt, bell(hz(mel[b]), 0.8), 0.22)
        t += 4 * beat
        bar += 1
    return buf


def write_wav(path, mono):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    w = wave.open(path, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(np.repeat((mono * 32767).astype(np.int16)[:, None], 2, axis=1).tobytes())
    w.close()
