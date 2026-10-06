# Image prompts for the human to run

The agent writes these; the human pastes them into an image generator (ChatGPT, or any tool
that returns transparent PNGs) and saves the results under the exact filenames given. Write
the prompts in English even when the project language is not: image models follow English
most reliably.

Deliver them as one Markdown file per episode: a short intro, one fenced block per image
with the filename and what to attach above it, a checklist table, and the fix phrases at
the end. Keep filenames lowercase with hyphens and no spaces, because the scene code loads
them by name.

## Contents

1. Style preamble (first message of the chat)
2. Character reference
3. A new pose for an existing character
4. Props, alone or on a sheet
5. Background
6. Fix phrases
7. How to keep the count down

## 1. Style preamble

The human sends this once, as the first message of a new image chat. It fixes the style for
every later image, which is what keeps twelve separately generated images looking like one set.

```text
In this chat I will ask you for a series of images for one animation. Use this exact
art style for EVERY image, and do not change it between images:

STYLE: Paper-cutout sticker asset for a stop-motion collage animation. Hand-painted
watercolor + colored-pencil children's-storybook illustration, cut out of watercolor
paper, with a thin clean white paper border following the whole silhouette (die-cut
sticker edge). Flat 2D, straight-on view, visible paper grain, soft pigment blooms,
loose darker pencil outlines. No 3D rendering, no photo texture, no glossy gradients,
no cast shadow, no ground, no scenery, no text.
PALETTE: tan, caramel, rust orange, cream, muted denim blue, olive, sage green, mustard,
tomato red, blush pink. Warm and gentle, never neon.
FACES: small solid black dot eyes, rosy blush circles on the cheeks, simple mouths.
BACKGROUND: every cutout is on a FULLY TRANSPARENT background (real alpha, not a
checkerboard pattern), single subject centered, whole subject visible with a generous
margin.

Reply "ready" and wait for my first request.
```

Adapt PALETTE to the project's characters. Everything else can stay.

## 2. Character reference

Make one reference image per character before anything else, and have the human show it to
you. Every later pose is generated against this image, so a wrong reference multiplies.

```text
Redraw the attached character in the STYLE above. Keep it recognizable: <three to six
features that define this character: silhouette, ears, face panel, colors, hair, tail>.
POSE: full body, standing, facing front, <a neutral or signature pose>.
```

If the character must read as a particular animal, name the features that say so (head
shape, ear size and placement, muzzle shape, nose, body proportions) and name the animal it
must not be mistaken for. Front views hide a lot; a side view often shows the species best.

## 3. A new pose for an existing character

The human attaches the character's reference image every time.

```text
The same <character> as the attached image, identical design, colors, patches and
proportions. New POSE: <view: front / side view facing left>, <what the body is doing>,
<expression>. <Small extras that belong to the drawing: sweat drops, a held object>.
```

Rules that save rework:

- Describe one pose per image, and say which way the character faces. Pick one facing
  direction per character and mirror in code when needed.
- If the character holds or pulls something the scene draws separately (a rope, a crank, a
  machine), say `Do NOT draw any <thing>` and have the paws grip thin air.
- If two poses must line up (same hanging point, same seat), attach the first pose when
  asking for the second and say `Same pose and same <anchor> as the attached image`.
- Small motion (sway, hop, squash, shiver, flip) is done in code from one image. Ask for a
  new image only when the body shape or the expression really changes.

## 4. Props

```text
In the same STYLE: <one object>, <view>, <materials and colors>. <Orientation: tall
portrait / wide landscape image>, the whole object visible. No face, no text.
```

Objects may have faces when it is funny (a smug cloud, a sleepy sun). For expressions of the
same object, attach the first image and say `Change only the face`, so the outlines match
and the scene can swap them in place.

Several small props can share one image; the prep script or a few lines of code can cut
them apart if they are well separated:

```text
In the same STYLE: a sheet of THREE separate sticker cutouts on one fully transparent
background, each with its own white die-cut border, clearly spaced apart with wide gaps
and not touching or overlapping:
1. <prop> 2. <prop> 3. <prop>
No faces, no text.
```

Anything that must spin or swing around a point needs that point in the middle of its own
image (a propeller separate from its stand, perfectly symmetrical and centered).

## 5. Background

The only opaque image. One per location is enough.

```text
A full-frame background, NOT a cutout and NOT transparent, <portrait / landscape>
orientation. Hand-painted watercolor on cold-press paper in a children's-storybook style:
<sky>, and at the bottom layered torn-paper hills in <colors>, each layer with a ragged
white torn-fiber edge and a slight shadow between layers. Soft warm vignette. No
characters, no trees, no objects, no text.
```

## 6. Fix phrases

Include these at the end of every prompt file.

- Checkerboard instead of transparency: `The background must be real transparency (alpha
  channel), not a drawn checkerboard. Regenerate.`
- Character drifted: attach the reference again, then `Match the attached reference
  exactly: same patches, same colors, same face. Only the pose changes.`
- Looks 3D or like a photographed toy: `Too 3D. Make it a flat 2D watercolor paper cutout,
  like a sticker.`
- Outline of a variant does not match: `Keep the exact same outline as the attached image.
  Only the face changes.`

## 7. Keeping the count down

A first episode needs about 12 images (two references, three poses each, a few props, one
background). A sequel in the same location needs 4 to 6. Plan the story around what already
exists: reuse the set, reuse poses, and let the ending of one episode be the opening frame
of the next.

Never ask for images of things the scene builds in code: title letters, paper tags and
their text, washi tape, dotted trails, speed lines, "!" and "?" marks, "z z z", rain drops,
flashes.
