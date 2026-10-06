# Style guide: paper-cutout storybook collage

Values that were used across a six-episode series. Treat them as defaults: change them for a
different project, but keep them constant within one series.

## Contents

1. Look
2. Colors and shadow
3. Type
4. Frame and layout
5. Motion
6. Sound
7. Story shape

## 1. Look

A hand-made paper collage in a children's-storybook style. Characters and props are
watercolor cutouts with a thin white die-cut border and a soft drop shadow, layered flat on
a painted paper background. Motion is snappy and playful, like stop-motion. On-screen text
is paper: tags held by tape, and titles made of mismatched letter tiles.

Avoid 3D, glossy gradients, photorealism, heavy blur or glow, and anything that drifts
smoothly at constant speed.

## 2. Colors and shadow

| Name | Value | Used for |
|---|---|---|
| tomato | `#d9483b` | "!" marks, underlines, accent word on tags, check marks |
| mustard | `#e0a73a` | tape, letters on dark tiles |
| teal | `#2f7f7a` | tape, tiles |
| ultramarine | `#2f4fa8` | "z z z", tiles |
| blush | `#f1a9a0` | tape, tiles |
| cream / paper | `#f3ecdf` / `#fbf7ee` | tags, text outlines |
| ink / pencil | `#2b2622` / `#3a332c` | text, drawn lines |
| night | `#1b2a4a` | a full-frame overlay at 0.3 opacity for storm or dusk |

Cutout shadow, on every cutout image:
`drop-shadow(0 9px 7px rgba(74,48,22,.3)) drop-shadow(0 2px 1.5px rgba(0,0,0,.2))`

Warm vignette over everything:
`radial-gradient(ellipse at 50% 46%, rgba(74,48,22,0) 58%, rgba(74,48,22,.26) 100%)`

## 3. Type

Three kinds of text only, and all of it short: a title, a label, a punchline word. Never
put dialogue on screen as full sentences unless the user asks for captions.

- **Title tiles.** One letter per paper tile, each tile a different color pair and font,
  rotated a random ±6° and nudged a few pixels, slapped on one at a time 0.07 s apart.
- **Tags.** Cream paper, dark text, a strip of semi-transparent tape on top, rotated 4 to 6°.
- **Marks.** "!", "?", "z" in a heavy display face with a thick paper-colored outline.

Fonts must contain the project's script. Ship them as local `.woff2` files next to the
scene so the render does not depend on the network. For Thai, this set works (all on
Google Fonts): Mali 700 for tags, Charm 700 for a brush caption, and Chonburi, Kanit 900,
Mitr 700, Itim, Sriracha, Pridi 700 mixed across the title tiles.

For scripts with combining marks (Thai, Devanagari, Arabic), split a title into letter
clusters by hand, for example `["เ","ค","รื่","อ","ง"]`, so a vowel or tone mark never lands
on a tile by itself.

## 4. Frame and layout

Vertical 1080×1920 at 30 fps for reels and shorts. Landscape is 1920×1080.

Values used for the vertical frame:

| Thing | Value |
|---|---|
| Ground line (characters' feet) | y = 1650 |
| Standing character | about 430 to 440 px tall |
| Foreground grass strip | from y = 1690 down, wider than the frame, in front of everything |
| Title tile | 122×150 px, 84 px letters, at most 5 per row |
| Safe margin for text | about 90 px from the frame edge |

Depth comes from layering: background, back props, characters, front props, a foreground
strip, drawn marks, tags, title, then overlays (dim, flash, vignette).

Build each character as a zero-size anchor point at the feet (or at the point it hangs
from), with nested wrappers inside it: one for idle sway, one fixed mirror for facing
direction, one for the paper-flip pose swap, then one image per pose stacked in place.
Moving the anchor moves the character; each wrapper owns one kind of transform, so tweens
never fight over the same property.

## 5. Motion

| Move | How | Time | Ease |
|---|---|---|---|
| Pop in | scale 0 and −12° to full size | 0.42 s | `back.out(2.6)` |
| Pose swap (paper flip) | scaleX 1→0, swap image, 0→1 | 0.07 + 0.14 s | `power2.in`, `back.out(3)` |
| Idle sway | ±2 to 4° back and forth, finite repeats | 0.9 to 1.5 s | `sine.inOut` |
| Drop in from above | y −1900 → 0 | 0.5 s | `bounce.out` |
| Land | scaleY 0.8 → 1 | 0.4 to 0.5 s | `elastic.out(1, 0.4)` |
| Hop | x eased, y up then down | 0.32 s | `power2.out` / `power2.in` |
| Camera shake | stepped seeded offsets, shrinking | 0.045 s per step | stepped |
| Camera push | scale 1 → 1.035 up to the twist | whole section | `sine.inOut` |
| Tag falls away | y +1300 or more, rotate 50 to 70°, then hide | 0.7 to 1.0 s | `power2.in` |
| Title | tiles from scale 1.9 to 1 | 0.07 s apart | `back.out(2.5)` |

Principles:

- Nothing on screen is ever completely still; give everything a small idle sway or bob.
- Anticipation, action, follow-through. Squash before a jump, overshoot after a landing.
- One sentence, one visual beat. Each reveal lands on, or just before, the word it shows.
- Do not put everything on screen at once; reveal across the scene.
- Deterministic rendering needs seeded randomness, finite repeat counts, and a timeline
  that can be sought to any frame.

## 6. Sound

- Music: a light plucked storybook loop around 100 BPM, 15 to 20 dB under the voice.
- Cut the music dead at the twist and bring it back for the end card. The silence is the
  punchline's drumroll.
- Effects are small and papery: pops for appearances, taps for letters and tags, a thud for
  drops, a boing for hops, a swish for wind and fast moves. Save big sounds for the one big
  moment.
- A voice from far away or from inside something: band-limit it, lower it, add a short echo.
- Target about −14 LUFS integrated, true peak under −1.5 dBTP.

## 7. Story shape

A 28 to 40 second clip holds one plan and one reversal:

1. Open on the problem (and, in a series, on the last frame of the previous episode).
2. The confident character unveils a contraption with a name on a tag.
3. It starts to work. A line of triumph.
4. It goes wrong in a way that follows from how it was built. Music stops.
5. The deadpan character benefits, or is untouched, and says very little.
6. Title tiles and a stamp-like tag.

Five to ten short lines in total. Let the picture carry the joke; a line of dialogue should
be something the picture cannot say.

For a series, repeat small rituals (the same tag wording, the same closing stamp) so they
become running gags, and plan a finale that breaks each ritual once.
