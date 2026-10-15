# Pose sheets: several poses in one picture

A sticker character is one picture for each pose. Asking the image tool for one picture at a
time gives the sharpest result but costs a request per pose, and each request draws the
character slightly differently. A pose sheet puts several poses in one picture. This file
says how many, how to get mouths that match, and how to cut the sheet.

Everything here was used in one finished episode (two characters, eleven pictures instead of
twenty) that the user accepted.

## How many poses on a sheet

**Three.** The image tool gives a picture about 1500 to 2000 pixels on its long side. What
matters is how tall each character comes out compared with how tall it is drawn on screen.

| Poses on one sheet | Height of each (pixels) | On a 1080 x 1920 screen at about 450 tall |
|---|---|---|
| 10 (2 rows of 5) | 380 to 440 | Enlarged almost twice in close shots; soft. Tried and dropped |
| 3 (one row) | 720 to 810 | Never enlarged. Used |
| 1 | 1000 and more | Sharpest; one request per pose |

A two-legged character goes three in a row on a landscape picture. A four-legged one, which
is wide, goes three in a column on a portrait picture.

The ten-pose sheet did keep the character's look the same across poses, and so does a sheet
of three. That is the real gain, more than the saved requests.

If the user wants to try a bigger sheet, let them: it is one request. Then cut it, put one
character on a frame at its real size, and show them. They judge from that, not from a
description.

## The prompt

Start from the character's reference picture and say, in this order: same character,
identical design; how many separate stickers and how they are arranged; each with its own
white die-cut border and a wide gap, not touching; all the same size and as tall as the
picture allows; the view and the direction they face; transparent background; no ground, no
glow, no labels, no numbers, no text. Then one short paragraph per pose, named by position
(LEFT, MIDDLE, RIGHT), each ending with the expression and whether the mouth is open or
closed.

Draw every pose with the mouth **closed** on this first sheet, except a pose that is only
ever seen shouting.

## Mouths that match

An open-mouth picture drawn on its own never lies on the closed one: the head tilts, an arm
moves, and the body jumps at every syllable. Asking for "the same pose but mouth open" on the
same sheet fails the same way.

What works: make the closed sheet first, then attach it and ask for an edit.

```text
Edit the attached image in place. Change ONLY the three mouths. LEFT: mouth now OPEN wide,
talking happily. MIDDLE: ... RIGHT: ... Everything else must stay pixel-for-pixel the same:
every head, ear, eye, arm, leg, patch and border, the size and the position of each
character. Do not move, resize or redraw anything else.
```

Even so, the tool redraws the whole picture a little and slides it by up to three pixels.
The mouths are right; everything else has changed slightly. So never use the edited sheet
whole. Build each open-mouth sticker like this:

1. Cut the closed sheet into stickers and keep each one's box and outline.
2. Slide the edited sheet until it lies on the closed one. Try every shift up to 14 pixels
   each way and keep the one with the smallest difference, measured away from the mouth.
3. Take the closed picture everywhere, and the edited one only inside a box round the mouth,
   with a soft edge of about six pixels.
4. Cut it with the closed sticker's box and outline.

Now the two pictures differ only at the mouth, and nothing else can move when they switch.

Give the mouth box by hand, from looking at the sheet. Finding it as "the place where the two
pictures differ most" picked a foot once and the whole sticker twice.

A character on the edited sheet whose mouth was not supposed to change is still redrawn. Take
those from the first sheet only.

## Cutting a sheet

- **Glow and specks.** The tool leaves a faint glow round each sticker and stray dots in the
  empty space. Treat opacity below about 110 of 255 as empty, and drop any separate piece
  smaller than a few hundred pixels.
- **Stickers that touch.** White borders often meet. Shrink the shapes until the right
  number of separate ones remains, then give every pixel to the nearest shrunken shape.
- **Order.** Sort by the middle of each shape along the row or column, and name them from
  the list of poses.
- **Check sheet.** Put the cut stickers in a row on a plain mid-green ground, all at one
  height, and look at it before building anything.

A script that does all of this for one episode exists in the project where it was first
used (`tools/prep_stickers.py`); it has the sheet names and mouth boxes written into it. It
has not yet been made general and added to this skill's `scripts/`. Until it is, copy it and
change the lists at the bottom.

## Props and machines

A prop that changes during the story is not a pose sheet; it is a set of separate pieces.
For a machine with a blade, a lever and a cake: the body with the moving parts left out and
the space they move in empty; the moving parts as their own stickers; the cake whole; the
cake in two (made by editing the whole one, so the halves match); the crumbs. Leave tags and
dials **blank**: image tools misspell Thai, and a needle has to turn. Draw the words, the
needle, a dashed guide line and anything that flies by code on top.

Measure where things attach (the plate, the rail, the middle of the dial) as fractions of the
body picture, not in pixels, because the picture may be scaled when it is packed.

## Acting with whole pictures

How a one-picture sticker sinks, arrives, hops and takes fright is in `animation-rules.md`.
