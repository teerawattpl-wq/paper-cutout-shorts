---
name: paper-cutout-shorts
description: Make short animated comedy or explainer clips (about 30 seconds, vertical or landscape) in a paper-cutout storybook style, end to end - story, two-voice dialogue with text-to-speech, image prompts for the user to generate, asset checks, a synthesized soundtrack, an HTML and GSAP scene, and a rendered MP4. Use this skill whenever the user wants an animated short, reel, cartoon episode, character skit, or a series of them built from code with their own characters, wants to continue or add an episode to such a series, or asks for cutout / stop-motion / sticker-style / storybook animation - even if they only say "make a clip with my characters" or "ทำคลิปแอนิเมชัน", "ทำการ์ตูนสั้น", "ทำตอนต่อไป". Also use it to turn a tutorial about AI-made animations into a working, low-cost pipeline.
compatibility: Needs a shell, Python 3.10+ (numpy, scipy, pillow), ffmpeg, and Node.js 18+ with the HyperFrames CLI (npx hyperframes). Needs a text-to-speech service (the bundled script uses the Gemini API; any TTS that returns audio files works). The user needs access to an image generator that can return transparent PNGs.
---

# Paper-cutout shorts

Build a short animated clip the way a small studio would, with the work split between the
agent and the user so that it costs almost nothing:

| Job | Who |
|---|---|
| Story, script, timing | agent |
| Voices | agent, through a TTS service |
| Character and prop images | **the user**, in an image generator, from prompts the agent writes |
| Checking and preparing images | agent |
| Music and sound effects | agent, synthesized in code |
| Animation and render | agent, as an HTML scene rendered to MP4 |
| Watching and listening to the result | **the user** |

The last row matters. An agent in this pipeline usually cannot watch motion or hear audio.
It can inspect still frames and transcripts, and nothing more. Say so every time a clip is
delivered, and list what the user should check with their own eyes and ears.

Work in the user's language. Write image prompts in English (image models follow it best).

## Before the first episode

Settle these with the user, briefly. Offer a recommendation for each instead of an open
question.

1. **Characters.** Two work best: one over-confident, one deadpan. Get the user's reference
   pictures, or agree on a description.
2. **Format.** Vertical 1080×1920 for reels and shorts, or landscape. Target length.
3. **Language** of the dialogue and on-screen text. This decides fonts and the TTS model.
4. **Reference clips**, if the user has a look or a channel in mind. Study structure
   (length, number of shots, how few words, where the twist lands) and take only that;
   write an original story with the user's own characters.
5. **TTS.** Confirm the service works in the chosen language with one short test line,
   before any creative work depends on it. Note the daily quota.

Check the tools once: `python --version`, `ffmpeg -version`, `node -v`,
`npx hyperframes --version`. If plain `python` is missing or hangs, use whatever launcher
the machine has (`python3`, `py`, `uv run --no-project --with numpy --with scipy --with pillow python`).

## Project layout

```
project/
  .env                     TTS key. Do not open it, print it, or copy it anywhere.
  images/                  character reference images, shared by all episodes
  scripts/                 copy this skill's scripts here once
  ep01/
    lines.json             the script: speakers, voices, delivery per line
    prompts.md             image prompts for the user
    images/                what the user generated for this episode
    audio/dialogue-raw.wav, audio/lines/01-<who>.wav ...
    video/index.html, timings.js, assets/, audio/, fonts/
  ep01-title-v1.mp4
```

One folder per episode. Later episodes copy `fonts/` and the HyperFrames project files
(`hyperframes.json`, `package.json`, `meta.json`, made once with `npx hyperframes init`)
from the previous one, and reuse its assets.

## The workflow for one episode

Move through these in order. There are two points where the user must act (images, final
viewing) and one where they must approve (the script). Outside those, keep going.

### 1. Story

Propose two or three story ideas in a small table: the plan, the reversal, and how many new
images each needs. Recommend one. Then write the chosen one as a shot table (picture, sound)
with five to ten short lines of dialogue. Read `references/style-guide.md` section 7 for
the story shape. In a series, open on the last frame of the previous episode and reuse its
set, which keeps the image count to four to six.

Wait for the user to approve the script. It is the cheapest thing to change now and the
most expensive later.

### 2. Voices

Write `lines.json` and generate all lines in one request:

```
python scripts/make_voice.py ep01/lines.json ep01/audio/dialogue-raw.wav
```

One request for the whole script keeps the voices consistent and respects small free
quotas. Do not regenerate without telling the user what it costs them.

Then cut the recording into lines:

```
python scripts/split_lines.py ep01/audio/dialogue-raw.wav                 # list segments
python scripts/split_lines.py ep01/audio/dialogue-raw.wav ep01/audio/lines 0.00-1.62:bear 5.10-8.08:camel ...
```

TTS models add things that are not in the script: breaths, stray syllables, a long tail of
noises, sometimes whole lines repeated. So transcribe each listed segment (any local
speech-to-text, for example faster-whisper with the language set) and match segments to
script lines before cutting. Keep only what matches. Report to the user any line whose
transcript does not match, and any non-speech sound you kept (a yawn, a laugh), because you
cannot hear whether it is right.

With a different TTS service, generate one file per line instead and skip the cutting. The
rest of the pipeline only needs `audio/lines/NN-<who>.wav`.

### 3. Image prompts

Write `prompts.md` for the user following `references/image-prompts.md`. For a first
episode this includes the style preamble and the two character references; stop after the
references and check them before the user makes the rest, since every later image copies
them.

Ask for as few images as the story allows. Do in code everything code can do (see the list
at the end of that reference).

### 4. Check and prepare the images

When the user says the images are in:

```
python scripts/prep_assets.py --src ep01/images --dst ep01/video/assets --sheet check.jpg \
    --new bear-ref,bear-fly,camel-ref --reuse ep00/video/assets:tree.png,grass.png
```

Read the report (missing files, no real transparency, subject touching the edge), then open
the contact sheet and look. Check that the character matches its reference, the pose is the
one asked for, and the facing direction is what the scene expects. Tell the user plainly
which images pass and which need redoing, with the fix phrase to paste.

### 5. Timing and sound

Write `video/timings.js` as a single object of named times:

```js
window.T = {"dur": 30, "l1": 1.4, "l2": 5.6, "twist": 13.3, "title": 22.6};
```

Place each line where its audio fits (you know every line's length), leave air after jokes,
and give the twist a named time. Both the soundtrack and the scene read this file, so a
timing change is made in one place.

Copy `scripts/mix_template.py`, edit its three marked sections, run it, then normalize:

```
python scripts/mix_ep01.py ep01
ffmpeg -i ep01/video/audio/mix.wav -af "loudnorm=I=-14:TP=-2:LRA=11" -ar 44100 ep01/video/audio/mix-final.wav
```

`scripts/synth.py` provides the sounds (pops, taps, thuds, a music loop, a snore) so no
audio files or licenses are needed. See the style guide, section 6, for how to use them.

### 6. The scene

Copy `references/scene-template.html` to `video/index.html` and build the episode in it.
Read `references/style-guide.md` sections 2 to 5 for colors, type, layout and motion values.

If the platform has HyperFrames skills or docs installed, read their current composition
rules first; the CLI evolves. The rules this template relies on:

- One paused GSAP timeline, registered as `window.__timelines["main"]`.
- The root element carries `data-composition-id`, `data-duration`, `data-width`, `data-height`;
  timed children carry `class="clip"`, `data-start`, `data-duration`, `data-track-index`.
- Deterministic: seeded random only, no `repeat: -1`, nothing built asynchronously.
- Audio is one `<audio class="clip">` element pointing at `mix-final.wav`.

Two mistakes cost the most time in practice:

- A `fromTo` that sets `opacity: 1` paints its start state immediately, so an element meant
  to appear at second 14 is visible from frame one. Pass `immediateRender: false`.
- Something that leaves the frame must travel far enough to clear it, and then be set to
  `opacity: 0`. Otherwise a corner of it sits at the edge for the rest of the clip.

### 7. Verify with stills

```
cd ep01/video
npx hyperframes lint
npx hyperframes snapshot --at 1.0,5.6,12.9,13.4,14.0,21.0,29.5 --no-end -o <temp dir>
```

Pick about ten times: one per shot, plus the frames just before and after the twist, plus
the end card. Open the contact sheet and check each frame against the shot table. Look
especially for: things visible before their cue, things poking in at the frame edge, text
running off the frame, tags or titles covering a face, hands not meeting what they hold.
Fix and re-snapshot only the affected times until the stills are right.

### 8. Render and deliver

```
npx hyperframes render --fps 30 --output ../../tmp-raw.mp4
ffmpeg -i tmp-raw.mp4 -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "ep01-title-v1.mp4"
```

The raw render is large; the second command brings it to a size that uploads comfortably.
Measure loudness on the final file (`ffmpeg -i file -af loudnorm=print_format=summary -f null -`)
and aim near −14 LUFS.

Tell the user:

- where the file is, its length and size;
- a timeline table of what happens when;
- what you verified (stills, transcripts) and what you could not (motion, sound);
- a short list of specific things to watch and listen for, most important first;
- how to ask for changes (timing lives in `timings.js`; a new voice take needs no new images).

Keep earlier versions when you revise: write `-v2`, do not overwrite `-v1`.

## Keeping a series going

- After each approved episode, add what you learned to a notes file in the project, and
  keep a handoff file current (status of each episode, open questions, quotas, pitfalls on
  this machine) so a fresh session can continue without the chat history.
- Agree on a season length early. A finale that pays off the running gags is worth planning
  for; six episodes was a good size.
- A change to a character's design is cheapest at a season boundary: every pose image has
  to be regenerated, though voices and scenes can be reused.

## Care with keys, quotas and other people's work

- The TTS key stays in the environment or `.env`. Never read it into the conversation, and
  remind the user to leave `.env` out when they share or zip the project.
- Free TTS tiers may use submitted text to improve the provider's products. Keep private
  material out of them.
- Rendering tools may collect usage statistics by default; offer to turn that off.
- Use the user's own characters and write original stories. A reference clip is for
  learning structure and pacing, and nothing from it should be copied into the script or
  the artwork.

## Bundled files

- `scripts/make_voice.py` - whole-script, two-voice TTS in one request (Gemini API).
- `scripts/split_lines.py` - list speech segments; cut chosen segments into line files.
- `scripts/prep_assets.py` - transparency and cropping checks, trimming, contact sheet.
- `scripts/synth.py` - synthesized sound effects and music; voice helpers. Imported by mixes.
- `scripts/mix_template.py` - soundtrack template to copy per episode.
- `references/style-guide.md` - look, colors, type, layout, motion, sound, story shape.
- `references/image-prompts.md` - prompt templates and fix phrases for the user's image tool.
- `references/scene-template.html` - the scene skeleton with character structure and helpers.
