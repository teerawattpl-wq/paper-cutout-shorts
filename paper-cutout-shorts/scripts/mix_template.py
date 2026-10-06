"""TEMPLATE: copy to your episode, then edit the three marked sections.

Builds <episode>/video/audio/mix.wav from the dialogue lines plus synthesized music and
sound effects. All times come from <episode>/video/timings.js, the same file the scene
reads, so picture and sound cannot drift apart.

Requires: numpy, scipy.   Usage (from the project root):
    python scripts/mix_template.py <episode_dir>
then bring it to the target loudness:
    ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-2:LRA=11" -ar 44100 mix-final.wav
"""
import io, json, os, re, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import synth as S

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
EP = sys.argv[1]
T = json.loads(re.search(r"\{.*\}", open(os.path.join(EP, "video", "timings.js"), encoding="utf-8").read()).group(0))
N = int(T["dur"] * S.SR)
voice, sfx = np.zeros(N), np.zeros(N)
L = os.path.join(EP, "audio", "lines")
p = lambda t, x, gain=1.0: S.put(sfx, t, x, gain)

# ---- 1. DIALOGUE: one entry per line file, placed at its key in timings.js ----------------
#      Wrap a line in S.far(...) when the speaker is far away or inside something.
for n, key, who in [(1, "l1", "bear"), (2, "l2", "bear"), (3, "l3", "camel")]:
    S.put(voice, T[key], S.load_line(os.path.join(L, "%02d-%s.wav" % (n, who))))

# ---- 2. MUSIC: a gain envelope over the loop. Cut it dead on the twist; bring it back -----
#      for the end card. Silence at the right moment is the strongest sound effect here.
music = S.music_loop(T["dur"])
ts = np.arange(N) / S.SR
g = np.clip(ts / 0.4, 0, 1)                                              # fade in
g = np.where((ts >= T["twist"]) & (ts < T["title"]), 0.0, g)             # silence after the twist
g = g * np.where(ts >= T["title"], np.clip((ts - T["title"]) / 0.3, 0, 1) * 1.5, 1.0)
g = g * np.clip((T["dur"] - ts) / 1.0, 0, 1)                             # fade out
music *= g

# ---- 3. SOUND EFFECTS: one call per event. Available in synth.py: pop, tap, thud, boing, ---
#      swish, rustle, whistle, bell, sparkle, snore, sweep/noise/filt/env for custom sounds.
p(0.2, S.swish(), 0.35)
p(T["twist"], S.thud(big=True), 1.0)
for i in range(9):                                                       # one tap per title tile
    p(T["title"] + i * 0.07, S.tap(), 0.7)
p(T["title"] + 1.5, S.sparkle(), 0.4)

# ---- final balance: music 15-20 dB under the voice ---------------------------------------
music *= S.rms(voice) * 10 ** (-16 / 20) / S.rms(music)
mix = np.tanh((voice + music + sfx * 0.5) * 1.1) / 1.1
mix = mix / np.abs(mix).max() * 0.89
out = os.path.join(EP, "video", "audio", "mix.wav")
S.write_wav(out, mix)
print("saved", out)
