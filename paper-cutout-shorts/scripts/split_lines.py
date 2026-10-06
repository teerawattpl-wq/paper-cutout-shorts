"""Find the spoken segments in a dialogue recording, and cut them into one file per line.

Requires ffmpeg on PATH.

1) List segments (speech between silences):
       python scripts/split_lines.py <raw.wav>
2) Cut chosen segments into files 01-<name>.wav, 02-<name>.wav, ...:
       python scripts/split_lines.py <raw.wav> <out_dir> 0.00-1.62:bear 5.10-8.08:bear 19.61-21.60:camel

Why two steps: TTS models add sounds that are not in the script (breaths, stray syllables,
whole repeated lines). List first, transcribe each segment to see which is which, then cut
only the segments that match the script. Add about 0.08 s of padding on each side.
"""
import io, os, re, subprocess, sys, wave

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def segments(path, noise="-38dB", min_silence=0.35):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af",
                        "silencedetect=noise=%s:d=%s" % (noise, min_silence), "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", p.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", p.stderr)]
    w = wave.open(path)
    total = w.getnframes() / w.getframerate()
    out, cur = [], 0.0
    for i, s in enumerate(starts):
        if s - cur > 0.05:
            out.append((cur, s))
        cur = ends[i] if i < len(ends) else total
    if total - cur > 0.05:
        out.append((cur, total))
    return out, total


def main():
    if len(sys.argv) == 2:
        segs, total = segments(sys.argv[1])
        print("total %.2f s, %d speech segments" % (total, len(segs)))
        for i, (a, b) in enumerate(segs, 1):
            print("%2d  %7.2f - %7.2f   (%.2f s)" % (i, a, b, b - a))
        return
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    raw, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for n, spec in enumerate(sys.argv[3:], 1):
        rng, name = spec.split(":")
        a, b = rng.split("-")
        dst = os.path.join(out_dir, "%02d-%s.wav" % (n, name))
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", a, "-to", b, "-i", raw, dst], check=True)
        print(dst, a, "-", b)


if __name__ == "__main__":
    main()
