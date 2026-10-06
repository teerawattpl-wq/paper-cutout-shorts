"""Generate a two-character dialogue with Gemini TTS in ONE request.

Usage (run from the project root):
    python scripts/make_voice.py <lines.json> <out.wav>

The API key is read from the environment variable GEMINI_API_KEY, or from a line
`GEMINI_API_KEY=...` in a `.env` file in the current directory. The key is never printed.

lines.json:
{
  "voices": {"Bear": "Puck", "Camel": "Gacrux"},
  "styles": {"Bear": "<base delivery for this speaker>", "Camel": "<...>"},
  "lines":  [{"speaker": "Bear", "text": "...", "style": "<delivery for this line>"}, ...]
}

A <long pause> is appended to every line so split_lines.py can cut the recording apart.
The free tier allows only a few requests per day, so the whole script goes in one request.
"""
import base64, io, json, os, sys, urllib.request, urllib.error, wave

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
MODEL = os.environ.get("GEMINI_TTS_MODEL", "gemini-3.8-flash-tts")


def load_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    if os.path.exists(".env"):
        for line in open(".env", encoding="utf-8-sig"):
            line = line.strip()
            if line.startswith("GEMINI_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("GEMINI_API_KEY not found in the environment or in ./.env")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    body = {
        "model": MODEL,
        "input": [{"type": "user_input", "content": [
            {"type": "text", "text": ln["text"] + " <long pause>",
             "annotations": [{"type": "speech_metadata", "speaker": ln["speaker"],
                              "style": spec["styles"][ln["speaker"]] + ", " + ln["style"]}]}
            for ln in spec["lines"]]}],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": {
            "mode": "conversational",
            "speakers": [{"speaker": s, "voice": v} for s, v in spec["voices"].items()]}},
    }
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/interactions",
        data=json.dumps(body).encode(),
        headers={"x-goog-api-key": load_key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("TTS_FAILED %s %s" % (e.code, e.read().decode("utf-8", "replace")[:800]))
    audio = [c for s in d.get("steps", []) if s.get("type") == "model_output"
             for c in s.get("content", []) if c.get("type") == "audio"]
    if not audio:
        sys.exit("NO_AUDIO " + json.dumps(d, ensure_ascii=False)[:800])
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as f:
        f.write(base64.b64decode(audio[-1]["data"]))
    w = wave.open(out)
    print("saved", out, "| seconds", round(w.getnframes() / w.getframerate(), 2))


if __name__ == "__main__":
    main()
