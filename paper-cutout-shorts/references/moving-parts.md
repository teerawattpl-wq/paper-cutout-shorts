# Moving parts: when one picture per pose is not enough

The style in this skill is stop-motion: a character is one picture per pose, and a change
of pose is a paper flip. That stays the default. This file is for the actions a flip
cannot do: an arm that waves and keeps waving, a paw that points at something moving, a
walk across the frame, a prop with a part that turns.

The rule of thumb: **flip the pose for acting, split the picture for action.** A change of
mood or stance is a new whole picture. Something a limb does over time is a separate piece
turning on a pivot.

Each method below says how far it has been tried. Do not promise the user a method marked
"not tried" without making a short test first.

## Which method for which need

| What the shot needs | Method | Extra pictures | Status |
|---|---|---|---|
| A new mood or stance | Flip to another whole pose (the default) | 1 per pose | Proven: six episodes |
| A mouth that moves while speaking, a blink | Swap set for the face | 2 or 3 with matching outlines | Proven in a sister project (a puppet with 12 heads) |
| An arm that waves, points or holds | Split the arm from the body; turn it on the shoulder | 1 or 2 pieces per arm, plus the body without that arm | The principle is proven in the sister project, where limbs are drawn lines; separate limb pictures are **not tried** in this style |
| A prop with a turning or swinging part | Split the part; its pivot at the middle of its own picture | 1 per part | Proven here (see image-prompts.md, section 4) |
| Breathing, hair or cloth moving a little | Warp one picture with a mesh | none | **Not tried.** No tool for it in this skill |

Count the pictures before choosing. The strength of this skill is how few pictures an
episode needs (four to six for a sequel). Splitting a whole character at every joint adds
about eight pieces per character, and every piece has to match the others in line and
colour. Split only the limb the story uses.

## 1. Pieces on pivots

The standard method of cut-out animation: the figure is cut at its joints, and each piece
turns around its own pivot.

- **Cut at the joint, with overlap.** The upper end of an arm is a rounded stub that sits
  under the edge of the body, so no gap opens when it turns. Ask for the arm "cut off
  cleanly at the shoulder with a rounded end".
- **The body must exist without the limb.** A body picture with the arm painted on cannot
  lose it. Ask for the pose again "with NO left arm; the shoulder is a clean edge", with the
  first picture attached so the rest matches.
- **Set the pivot once, before any motion.** In the scene the pivot is `transform-origin`,
  given in pixels of the piece's own picture (the shoulder end, not the centre). Changing a
  pivot after keys exist is the usual reason pieces drift apart; the makers of cut-out
  software say the same of their tools.
- **Parent pieces in order.** A forearm sits inside the upper arm's element, a paw inside
  the forearm's, so turning the shoulder carries everything below it. This is the same
  nesting the character already uses (anchor > sway > mirror > poses): add one wrapper per
  joint and let each wrapper own one transform.
- **Shadows.** The cutout shadow is a filter on each picture. Pieces that overlap will
  shadow each other at the joint; put the filter on the wrapper that holds all pieces of the
  figure instead.
- **The white border.** A die-cut border on every piece draws a white line across each
  joint. Either ask for pieces without a border and let one outer wrapper carry the look, or
  accept the line as part of the paper style. Decide before the pictures are made.

A lighter variant that has been used for a whole film: keep the head, body, paws and feet
as pictures and draw the limbs between them as plain lines in code. It needs no limb
pictures and a paw can reach any point, but it only suits a character designed with
stick-like limbs.

## 2. Swap sets

Some parts look wrong when turned or stretched and are drawn several times instead.

- **Mouth.** Two or three pictures of the same head that differ only in the mouth. Deforming
  one mouth is awkward; cut-out studios keep a bank of mouth drawings and swap them.
- **Paws and hands.** A small set (open, pointing, gripping, fist) swapped at the end of
  the arm is easier than moving fingers and looks less mechanical.
- **Eyes.** One set for where the pupils look, a separate set for lids and blinks.

What makes a swap work:

- The outlines must match exactly, or the head jumps. Attach the first picture and say
  `Keep the exact same outline as the attached image. Only the face changes.`
- Generate the whole set in one picture, as a grid, when the tool allows it: pieces made
  together match better than pieces made one at a time.
- Hide the change inside a movement: a few degrees of turn, a small stretch or skew over
  the two or three frames around the swap. The paper flip already does this for whole
  poses.
- For speech, open the mouth on the loud part of each syllable, not on a fixed rhythm.

## 3. Warping one picture

Animation software such as Moho, Spine and Live2D lays a mesh of triangles over a picture
and moves the mesh's points, so one picture bends without being cut. It suits small
continuous movement: breathing, a tail, hair, cloth. It does not replace cutting for large
moves: an arm that crosses the body still needs the part of the body it covers, and
bending one picture with bones alone tends to look poor on complex shapes.

Nothing in this skill does this. A scene is HTML and CSS transforms, which move and turn
whole pictures. Two cheap stand-ins that are within reach: a slow `scaleY` of one or two
per cent anchored at the feet for breathing, and a `skewX` of a degree or two on hair or a
flag.

## Tools that split a flat picture into layers

There are services that take a flat character picture and return separate layers (hair,
face, clothes, limbs) with the hidden areas painted in. From their own descriptions:

- they give layers, not a rig: no pivots, no bones, no mesh;
- fine edges and parts that overlap heavily may need cleaning by hand;
- the painted-in hidden areas are guesses and should be looked at.

**Not tried here, and the information comes from the sellers.** No independent test was
found. If one is used, treat its output like any other picture from the user: run it
through `prep_assets.py`, look at the contact sheet, and check each piece against the
reference before building on it.

## What makes motion smooth, pieces or not

Splitting makes a move possible. How the move is timed makes it smooth, and these apply to
whole-pose flips as well:

- **Ease.** Start slow, move fast, arrive slow. Never a constant speed.
- **Overlap.** Parts of a figure start and stop at different moments: the body arrives,
  then the head settles, then an ear. Offset each part by two to four frames.
- **Squash and stretch.** A few per cent of squash when feet land, a little stretch on the
  way up.
- **Anticipation.** A small move the other way before the main one.
- **Arcs.** A paw travels on a curve, which turning on a pivot gives for free; do not slide
  a hand in a straight line.

Stop-motion snap and these principles do not conflict. A snappy move is a short eased move
with an overshoot, not a move at constant speed.

## Prompts for pieces

```text
The same <character> as the attached image, identical design and colors, same pose, but
with NO <left arm>: the <left shoulder> is a clean edge with nothing attached.
```

```text
In the same STYLE: ONLY the <left arm> of the attached <character>, alone, <straight,
hanging down>, cut off cleanly at the shoulder with a rounded end, the paw at the bottom.
The shoulder end at the top center of the image. Nothing else in the image.
```

```text
In the same STYLE: a sheet of THREE separate cutouts of the SAME head of the attached
<character>, same size, same outline, facing the same way, clearly spaced apart:
1. mouth closed  2. mouth half open  3. mouth wide open.  Only the mouth changes.
```

Check on the contact sheet: the piece's joint end is where the prompt put it, the colours
match the body, and the three heads are the same size.

## Sources

Principles of cut-out rigging, swap sets and easing, from the makers of animation software
and their user forums:

- Toon Boom Harmony: [setting up the pivots](https://docs.toonboom.com/help/harmony/Content/HAR/Stage/018_Deformation/059i_H3_Setting_Up_the_Pivots.html),
  [animating with the Transform tool](https://docs.toonboom.com/help/harmony-24/premium/cut-out-animation/about-transform-tool.html),
  [swapping drawings](https://docs.toonboom.com/help/harmony-21/premium/cut-out-animation/about-swap-drawing.html),
  [studying the model](https://docs.toonboom.com/help/animate-pro/Content/HAR/Stage/011_Character_Building/009_H1_Studying_the_Model.html)
- Toon Boom forum: [parenting body parts and pivot points](https://forums.toonboom.com/t/parenting-body-parts-and-pivot-point-problem/8095),
  [cutout animation](https://forums.toonboom.com/t/cutout-animation/2300)
- Spine forum: [more than one bone for one image](https://ko.esotericsoftware.com/forum/d/39-more-than-one-bone-for-one-image)
- Moho: [animating a single illustration with mesh warp](https://lesterbanks.com/?p=64240)
- PixelOver: [2D mesh deformation](https://docs.pixelover.io/tutorials/mesh_deformation/)
- [Overlapping action](https://brush.ninja/glossary/animation/overlapping-action/), a glossary entry
