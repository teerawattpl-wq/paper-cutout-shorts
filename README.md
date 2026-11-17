# paper-cutout-shorts

An agent skill for making short animated clips (about 30 seconds) in a paper-cutout
storybook style, from story to rendered MP4.

สกิลสำหรับเอเจนต์ AI ใช้ทำคลิปแอนิเมชันสั้นสไตล์กระดาษตัดแปะ ตั้งแต่เขียนเรื่องจนได้ไฟล์ MP4

## What it does

The work is split so it costs almost nothing:

| Job | Who |
|---|---|
| Story, script, timing | the agent |
| Voices | the agent, through a text-to-speech service |
| Character and prop images | you, in an image generator, from prompts the agent writes |
| Music and sound effects | the agent, synthesized in code |
| Animation and render | the agent, as an HTML scene rendered with HyperFrames |

## What you need

- Python 3.10+ with `numpy`, `scipy`, `pillow`
- `ffmpeg`
- Node.js 18+ (the HyperFrames CLI runs through `npx hyperframes`)
- A text-to-speech service. The bundled script uses the Gemini API and reads the key from
  the `GEMINI_API_KEY` environment variable or a local `.env` file.
- An image generator that can return transparent PNGs

## Install

The skill is the folder [`paper-cutout-shorts/`](paper-cutout-shorts/). It follows the
common agent-skill layout: a `SKILL.md` with a name and description, plus `scripts/` and
`references/`.

- **Claude Code:** copy the folder into `.claude/skills/` in your project or home directory.
- **Any other agent:** put the folder in your project and tell the agent:
  "Read `paper-cutout-shorts/SKILL.md` and follow it."

## Contents

| File | Purpose |
|---|---|
| `SKILL.md` | The workflow for one episode, and how the work is shared with the user |
| `references/style-guide.md` | Look, colors, type, layout, motion, sound, story shape |
| `references/image-prompts.md` | Prompt templates and fix phrases for the image generator |
| `references/scene-template.html` | Scene skeleton with character structure and helpers |
| `references/moving-parts.md` | Pieces on pivots, swap sets and warping, for actions a pose swap cannot do |
| `references/pose-sheets.md` | Several poses of a character in one picture, and how to cut them apart |
| `references/animation-rules.md` | The eight classic rules of animation, with the numbers that worked |
| `scripts/make_voice.py` | Whole-script, two-voice TTS in one request |
| `scripts/split_lines.py` | Find speech segments and cut them into one file per line |
| `scripts/prep_assets.py` | Transparency and cropping checks, trimming, contact sheet |
| `scripts/synth.py` | Synthesized sound effects and music |
| `scripts/mix_template.py` | Soundtrack template to copy per episode |

## Notes

- Never commit your `.env` file or API key.
- Use your own characters and write your own stories.

## License

MIT. See [LICENSE](LICENSE).
