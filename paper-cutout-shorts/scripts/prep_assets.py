"""Check hand-made cutout images, trim their transparent margins, and build a contact sheet.

Requires: pillow, numpy.

Usage (run from the project root):
    python scripts/prep_assets.py --src ep02/images --dst ep02/video/assets --sheet check.jpg \
        --new bear-leaf,camel-sleep,leaf \
        --reuse ep01/video/assets:tree.png,grass.png,bg-sky.jpg

For every name in --new it reports: missing files, whether the image has real transparency
(image generators sometimes paint a checkerboard instead), and whether the subject touches
the image edge (probably cropped). Trimmed copies go to --dst; originals are never modified.
Files listed in --reuse are copied as they are. Open the contact sheet and LOOK at it before
building the scene: a file can pass every check and still be the wrong drawing.

A background image (opaque, full frame) should not go through --new. Crop it to the frame
size separately and put it in --dst.
"""
import argparse, io, os, shutil, sys
import numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PAD = 6

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--dst", required=True)
ap.add_argument("--sheet", required=True)
ap.add_argument("--new", default="")
ap.add_argument("--reuse", nargs="*", default=[])
a = ap.parse_args()

os.makedirs(a.dst, exist_ok=True)
want = [w for w in a.new.split(",") if w]
have = {os.path.splitext(f)[0].lower(): f for f in os.listdir(a.src)}
print("files:", sorted(have.values()))
print("MISSING:", [w for w in want if w not in have])
tiles = []
for name in want:
    if name not in have:
        continue
    im = Image.open(os.path.join(a.src, have[name]))
    mode = im.mode
    im = im.convert("RGBA")
    alpha = np.array(im)[..., 3]
    clear = (alpha < 10).mean() * 100
    if clear < 5:
        print("%-18s %s %s  NO REAL TRANSPARENCY (%.0f%% clear) - ask for it to be regenerated" % (name, im.size, mode, clear))
        continue
    ys, xs = np.where(alpha > 10)
    edge = xs.min() <= 1 or ys.min() <= 1 or xs.max() >= im.width - 2 or ys.max() >= im.height - 2
    box = (max(xs.min() - PAD, 0), max(ys.min() - PAD, 0), min(xs.max() + PAD + 1, im.width), min(ys.max() + PAD + 1, im.height))
    out = im.crop(box)
    out.save(os.path.join(a.dst, name + ".png"))
    print("%-18s %s %s transparent %.0f%% -> %s%s" % (name, im.size, mode, clear, out.size, "  TOUCHES-EDGE" if edge else ""))
    t = out.copy()
    t.thumbnail((440, 440))
    bg = Image.new("RGBA", (460, 460), (40, 90, 160, 255))   # a strong colour shows white borders and holes
    bg.alpha_composite(t, ((460 - t.width) // 2, (460 - t.height) // 2))
    tiles.append(bg.convert("RGB"))
for spec in a.reuse:
    d, files = spec.split(":")
    for f in files.split(","):
        shutil.copyfile(os.path.join(d, f), os.path.join(a.dst, f))
if tiles:
    sheet = Image.new("RGB", (460 * len(tiles), 460))
    for i, t in enumerate(tiles):
        sheet.paste(t, (i * 460, 0))
    sheet.save(a.sheet, quality=88)
    print("contact sheet:", a.sheet)
