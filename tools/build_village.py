#!/usr/bin/env python3
"""
Compose a dense, shadowed, organic village PNG from the Sparklin Labs
Ninja Adventure tileset (CC0).

Cares this revision tries to handle:
 - Grass tile has a directional blade pattern. Tiling it 1:1 produces
   visible vertical stripes (every 16 px). We break the seam by
   randomly flipping each tile horizontally and vertically.
 - The cross path was perfectly straight + sharp corners, which reads
   as "tile editor", not "lived-in village". Path is now a winding
   strip with a sine-wave deviation and a rounded intersection.
 - Objects looked stuck on top of grass. We darken the grass directly
   under each tree/house (ambient occlusion patch) and add a softer
   drop shadow on top.
 - Tile borders (grass/dirt) softened with grass tufts AND random dirt
   patches scattered just outside the path (foot-traffic wear).
"""

from __future__ import annotations

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(21)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TILESET_PATH = os.path.join(ROOT, "assets", "sparklin", "ninja_tileset.png")
OUT_PATH = os.path.join(ROOT, "assets", "sprites", "village_background.png")

TILE = 16
tileset = Image.open(TILESET_PATH).convert("RGBA")


def tile(col: int, row: int) -> Image.Image:
    x, y = col * TILE, row * TILE
    return tileset.crop((x, y, x + TILE, y + TILE))


def chunk(col: int, row: int, w: int, h: int) -> Image.Image:
    x, y = col * TILE, row * TILE
    return tileset.crop((x, y, x + w * TILE, y + h * TILE))


GRASS      = (14, 16)            # clean grass, no black seam
GRASS_ALT  = (13, 16)            # yellow-dappled variant
DIRT       = (21, 16)
WATER      = (20, 8)

HOUSES = [
    chunk(0,  0, 4, 3),
    chunk(4,  0, 4, 3),
    chunk(8,  0, 4, 3),
    chunk(12, 0, 4, 3),
]

def _strip_dirt_base_chunk(img: Image.Image) -> Image.Image:
    """Same as _strip_dirt_base but inlined for the trees at module
    load time (trees are defined before _strip_dirt_base in the file).
    Red-dominant pixels are made transparent so the rectangular dirt
    patch baked under each tree doesn't read on grass."""
    out = img.copy().convert("RGBA")
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if r > 110 and g < 100 and b < 90 and (r - g) > 35:
                px[x, y] = (0, 0, 0, 0)
    return out


TREE_ROUND = _strip_dirt_base_chunk(chunk(4, 10, 2, 2))
TREE_DARK  = _strip_dirt_base_chunk(chunk(8, 10, 2, 2))
TREE_LEFT  = _strip_dirt_base_chunk(chunk(0, 10, 2, 2))
TREE_PINE  = _strip_dirt_base_chunk(chunk(6, 10, 2, 2))
# Mix of "tree" sized things (2x2) — some entries duplicated to weight the mix.
TREES_BIG = [TREE_ROUND, TREE_DARK, TREE_LEFT, TREE_PINE]
# Mid-size: just the big bush — slots between trees to break the grid.
MID_FILLERS = []  # populated after BUSH_BIG is defined (see below)

CHERRY_BIG = chunk(4, 16, 2, 2)
CHERRY_SM  = chunk(8, 16, 2, 2)

def _strip_dirt_base(img: Image.Image) -> Image.Image:
    """Make the red-brown 'dirt soil' pixels around a plant transparent.
    These single-tile sprites were drawn for dirt backgrounds, so a
    rusty soil ring is baked into the bottom 2-3 rows. On grass that
    ring reads as a misplaced tiny brown rectangle — we drop it here."""
    out = img.copy().convert("RGBA")
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            # Red-brown dirt: red dominant, low green & blue
            if r > 110 and g < 100 and b < 90 and (r - g) > 35:
                px[x, y] = (0, 0, 0, 0)
    return out


BUSH_SM    = _strip_dirt_base(tile(3, 13))
BUSH_BIG   = tile(9, 15)              # already clean — no soil base
GRASS_TUFT = _strip_dirt_base(tile(4, 15))
SUNFLOWER  = _strip_dirt_base(tile(3, 15))
STONE_BIG  = chunk(14, 11, 2, 2)
STONE_SM   = tile(13, 11)
FENCE_H    = chunk(5, 4, 3, 2)       # horizontal fence segment

# Now that BUSH_BIG and BUSH_SM exist, fill the filler list
MID_FILLERS = [BUSH_BIG, BUSH_BIG, BUSH_SM]


def stamp(canvas: Image.Image, img: Image.Image, x_px: int, y_px: int) -> None:
    canvas.alpha_composite(img, (x_px, y_px))


def random_flip(img: Image.Image) -> Image.Image:
    if random.random() < 0.5:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if random.random() < 0.5:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    return img


def random_hflip(img: Image.Image) -> Image.Image:
    """Horizontal flip only — used for objects that have an "up" direction
    (houses, trees, bushes) so they don't end up upside-down."""
    if random.random() < 0.5:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


def feather_path_edges(canvas: Image.Image, path_cells: set,
                       cols: int, rows: int) -> None:
    """For each grass cell adjacent to a path cell, paint a soft brown haze
    so the dirt visually 'creeps' into the grass instead of stopping at a
    knife-sharp grid line. Done as a single feathered PIL layer that's
    blurred and then composited on the canvas."""
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for (tx, ty) in path_cells:
        for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1),
                         (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            nx, ny = tx + ddx, ty + ddy
            if (nx, ny) in path_cells:
                continue
            if 3 <= nx < cols and 0 <= ny < rows:
                # Brown halo blob, alpha varies a bit per cell
                a = 55 + random.randint(-15, 15)
                d.ellipse(
                    [nx * TILE - 3, ny * TILE - 3,
                     nx * TILE + TILE + 3, ny * TILE + TILE + 3],
                    fill=(120, 85, 50, a),
                )
    layer = layer.filter(ImageFilter.GaussianBlur(radius=5.5))
    canvas.alpha_composite(layer)


def darken_path_edges(canvas: Image.Image, path_cells: set) -> None:
    """Slight per-tile brightness variation on dirt tiles + darker shadow
    on outermost path cells so the path has 'worn center, shaded edges'."""
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for (tx, ty) in path_cells:
        on_edge = any(
            (tx + ddx, ty + ddy) not in path_cells
            for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        )
        if on_edge:
            a = 50 + random.randint(-10, 10)
            d.rectangle(
                [tx * TILE, ty * TILE, tx * TILE + TILE, ty * TILE + TILE],
                fill=(40, 25, 15, a),
            )
        elif random.random() < 0.18:
            # occasional lighter "sun-bleached" center tile
            d.rectangle(
                [tx * TILE, ty * TILE, tx * TILE + TILE, ty * TILE + TILE],
                fill=(255, 230, 180, 25),
            )
    layer = layer.filter(ImageFilter.GaussianBlur(radius=1.2))
    canvas.alpha_composite(layer)


def draw_shadow(canvas: Image.Image, cx: int, cy: int, rx: int, ry: int,
                alpha: int = 90, blur: float = 1.5) -> None:
    pad = 6
    layer = Image.new("RGBA", (rx * 2 + pad * 2, ry * 2 + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([pad, pad, pad + rx * 2, pad + ry * 2], fill=(0, 0, 0, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=blur))
    canvas.alpha_composite(layer, (cx - rx - pad, cy - ry - pad))


def darken_grass_patch(canvas: Image.Image, cx: int, cy: int, rx: int, ry: int,
                       alpha: int = 55) -> None:
    """Ambient-occlusion patch — same as shadow but greener tint and softer."""
    pad = 8
    layer = Image.new("RGBA", (rx * 2 + pad * 2, ry * 2 + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([pad, pad, pad + rx * 2, pad + ry * 2], fill=(30, 60, 30, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=2.5))
    canvas.alpha_composite(layer, (cx - rx - pad, cy - ry - pad))


def main() -> None:
    cols, rows = 80, 48
    W, H = cols * TILE, rows * TILE
    cx, cy = cols // 2, rows // 2

    bg = Image.new("RGBA", (W, H), (90, 140, 70, 255))
    grass = tile(*GRASS)
    grass_alt = tile(*GRASS_ALT)
    dirt = tile(*DIRT)
    water = tile(*WATER)

    # 1) Grass base: blend plain + dappled grass in soft Perlin-ish patches
    # so the field has tonal variation instead of one flat green.
    # Cheap "patch" generator: blob centers, anything within radius uses alt.
    alt_centers = [(random.randint(3, cols - 1), random.randint(0, rows - 1))
                   for _ in range(28)]
    for ty in range(rows):
        for tx in range(cols):
            # alt if inside any patch, otherwise plain
            in_patch = False
            for (acx, acy) in alt_centers:
                dx = tx - acx
                dy = ty - acy
                if dx * dx + dy * dy < 9:        # radius ~3
                    in_patch = True
                    break
            base = grass_alt if in_patch and random.random() < 0.65 else grass
            bg.paste(random_flip(base), (tx * TILE, ty * TILE))

    # 2) River on left. Tried scattering pebble tiles along the bank,
    # but tile (13,11) — which I labeled STONE_SM — is actually a
    # brown wooden block and read as a row of brown rectangles next to
    # the blue water. Removed until a real pebble tile is identified.
    for ty in range(rows):
        for tx in range(3):
            bg.paste(random_flip(water), (tx * TILE, ty * TILE))

    # 3) Winding paths instead of a rigid cross.
    # Vertical path: center column cx with a slow sine deviation.
    # Horizontal path: center row cy with deviation.
    PATH_HALF = 2  # half-width (3 tiles total when half=1; we use 2 → 5 wide)
    PLAZA_R = 5    # center-clearing radius in tiles; paths skip this disc

    def in_plaza(tx: int, ty: int) -> bool:
        dx = tx - cx
        dy = ty - cy
        return dx * dx + dy * dy <= PLAZA_R * PLAZA_R

    path_cells: set[tuple[int, int]] = set()

    def add_path_cell(tx: int, ty: int) -> None:
        if 3 <= tx < cols and 0 <= ty < rows and not in_plaza(tx, ty):
            path_cells.add((tx, ty))

    # Vertical strip — bigger wobble, variable width
    for ty in range(rows):
        offset = int(3.5 * math.sin(ty / 5.0)) + int(2 * math.cos(ty / 11.0))
        center = cx + offset
        half = PATH_HALF + (1 if (ty % 7 == 0) else 0)
        for dx in range(-half, half + 1):
            add_path_cell(center + dx, ty)

    # Horizontal strip
    for tx in range(3, cols):
        offset = int(3.5 * math.sin(tx / 7.0)) + int(2 * math.cos(tx / 13.0))
        center = cy + offset
        half = PATH_HALF + (1 if (tx % 8 == 0) else 0)
        for dy in range(-half, half + 1):
            add_path_cell(tx, center + dy)

    # Stamp path
    for (tx, ty) in path_cells:
        bg.paste(random_flip(dirt), (tx * TILE, ty * TILE))

    # Mark plaza cells as "occupied" so trees/bushes/houses skip them too.
    plaza_cells: set[tuple[int, int]] = set()
    for ty in range(rows):
        for tx in range(cols):
            if in_plaza(tx, ty):
                plaza_cells.add((tx, ty))

    def on_path(tx: int, ty: int) -> bool:
        return (tx, ty) in path_cells

    def near_path(tx: int, ty: int, dist: int = 1) -> bool:
        for ddy in range(-dist, dist + 1):
            for ddx in range(-dist, dist + 1):
                if (tx + ddx, ty + ddy) in path_cells:
                    return True
        return False

    # Foot-traffic wear DISABLED — was creating isolated brown blobs far
    # from the main path. Path is now strictly the planned strip + edge
    # feathering for the soft boundary.

    # Path tonal shading — darker edges, occasional bright center
    darken_path_edges(bg, path_cells)
    # Brown haze blending path into grass (the "no hard cut" effect)
    feather_path_edges(bg, path_cells, cols, rows)

    # 4) Houses with AO patch + drop shadow + doorstep.
    placements = [
        (HOUSES[0], 7,  7),
        (HOUSES[1], 16, 6),
        (HOUSES[2], 27, 7),
        (HOUSES[3], 47, 6),
        (HOUSES[0], 56, 7),
        (HOUSES[1], 67, 8),
        (HOUSES[3], 7,  27),
        (HOUSES[2], 16, 29),
        (HOUSES[0], 27, 27),
        (HOUSES[1], 47, 29),
        (HOUSES[3], 58, 27),
        (HOUSES[2], 68, 29),
    ]
    house_rects = []
    occupied: set[tuple[int, int]] = set(plaza_cells)  # plaza is off-limits

    for (img, tx, ty) in placements:
        if on_path(tx, ty) or on_path(tx + img.size[0] // TILE - 1, ty):
            continue
        if any(on_path(tx + dx, ty + dy)
               for dx in range(img.size[0] // TILE)
               for dy in range(img.size[1] // TILE)):
            continue
        px, py = tx * TILE, ty * TILE
        # Soft front yard: a feathered brown patch (not a hard 2-tile dirt
        # rectangle) right under the door, with grass tufts breaking its edge.
        door_tx = tx + img.size[0] // TILE // 2 - 1
        door_ty = ty + img.size[1] // TILE
        yard_layer = Image.new("RGBA", (TILE * 4, TILE * 3), (0, 0, 0, 0))
        yard_d = ImageDraw.Draw(yard_layer)
        yard_d.ellipse([4, 4, TILE * 4 - 4, TILE * 3 - 4],
                       fill=(155, 100, 55, 220))
        yard_layer = yard_layer.filter(ImageFilter.GaussianBlur(radius=4))
        bg.alpha_composite(yard_layer,
                           (door_tx * TILE - TILE, door_ty * TILE - 4))
        # AO under building (subtle wider green darkening)
        ao_cx = px + img.size[0] // 2
        ao_cy = py + img.size[1] - 2
        darken_grass_patch(bg, ao_cx + 2, ao_cy, img.size[0] // 2 + 6, 10)
        # drop shadow (offset right for sun from upper-left)
        draw_shadow(bg, ao_cx + 6, ao_cy, img.size[0] // 2, 6, alpha=120, blur=2.0)
        # Do NOT h-flip houses — they have asymmetric details (chimneys,
        # door positions, window styles) that look wrong mirrored.
        stamp(bg, img, px, py)
        house_rects.append((px, py, img.size[0], img.size[1]))
        for ddy in range(img.size[1] // TILE):
            for ddx in range(img.size[0] // TILE):
                occupied.add((tx + ddx, ty + ddy))

    def overlaps_house(px, py, w=16, h=16) -> bool:
        for (hx, hy, hw, hh) in house_rects:
            if px + w > hx and px < hx + hw and py + h > hy and py < hy + hh:
                return True
        return False

    # 5) Forest — varied sizes (big tree / mid bush / cherry), per-object
    # y-jitter so they don't stack into a perfect grid row.
    def place_object(tx: int, ty: int, obj_img: Image.Image,
                     y_jitter: int = 3,
                     hflip: bool = False) -> bool:
        cw = obj_img.size[0] // TILE
        ch = obj_img.size[1] // TILE
        if on_path(tx, ty) or near_path(tx, ty, dist=0):
            return False
        # Stricter house exclusion — entire tree bounding box must be clear
        # of any house, with 8px safety margin so tree canopies don't
        # overlap house walls.
        for (hx, hy, hw, hh) in house_rects:
            if (tx * TILE + obj_img.size[0] > hx - 8 and
                tx * TILE < hx + hw + 8 and
                ty * TILE + obj_img.size[1] > hy - 8 and
                ty * TILE < hy + hh + 8):
                return False
        for ddy in range(ch):
            for ddx in range(cw):
                if (tx + ddx, ty + ddy) in occupied:
                    return False
        # y-jitter — break the strict grid row
        jy = random.randint(-y_jitter, y_jitter)
        px = tx * TILE
        py = ty * TILE - TILE + jy
        trunk_x = px + obj_img.size[0] // 2
        trunk_y = py + obj_img.size[1] - 4
        # AO patch is FATTER than the tree base so the brown trunk pixels
        # always sit on a darkened grass disc, not on raw bright grass.
        darken_grass_patch(bg, trunk_x + 1, trunk_y,
                           obj_img.size[0] // 2 + 4, 8, alpha=85)
        draw_shadow(bg, trunk_x + 3, trunk_y,
                    obj_img.size[0] // 2 + 1, 5, alpha=130, blur=2.5)
        stamped = obj_img.transpose(Image.FLIP_LEFT_RIGHT) if hflip else obj_img
        stamp(bg, stamped, px, py)
        for ddy in range(ch + 1):
            for ddx in range(cw):
                occupied.add((tx + ddx, ty + ddy - 1))
        return True

    def pick_forest_obj(depth: int, allow_cherry: bool):
        """Return (img, hflip_ok). Cherry trees disabled — at the camera
        zoom we're using, their pink 32×32 sprite reads as a red
        rectangle next to other red elements (house roofs) and looked
        broken. Stick to green trees for a unified forest tone."""
        del allow_cherry  # no longer used
        r = random.random()
        if r < 0.10:
            return (random.choice(MID_FILLERS), False)
        return (random.choice(TREES_BIG), random.random() < 0.5)

    # Outer ring — smooth probability falloff instead of cliff at depth=5
    for ty in range(0, rows, 2):
        for tx in range(3, cols, 2):
            depth = min(ty, rows - 1 - ty, cols - 1 - tx)
            # density: 0.92 at edge, fading to 0.05 by depth 8
            density = max(0.05, 0.92 - depth * 0.115)
            if random.random() < density:
                obj, hflip = pick_forest_obj(depth, allow_cherry=False)
                place_object(tx, ty, obj, hflip=hflip)

    # Cherry-blossom-near-house pass disabled — same reason.

    # 6a) Flower beds — pick a dozen cluster centers in open grass and
    # scatter 4-8 sunflowers around each so they read as flower beds
    # rather than randomly sprinkled single flowers.
    flowerbeds = 0
    attempts = 0
    while flowerbeds < 4 and attempts < 100:
        attempts += 1
        cxx = random.randint(8, cols - 8)
        cyy = random.randint(6, rows - 7)
        if on_path(cxx, cyy) or near_path(cxx, cyy, 3):
            continue
        if (cxx, cyy) in occupied or overlaps_house(cxx * TILE, cyy * TILE, 64, 64):
            continue
        # Plant a small tight cluster (3-5 instead of 4-8)
        n = random.randint(3, 5)
        planted = 0
        for _ in range(n * 2):
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            ftx, fty = cxx + dx, cyy + dy
            if 4 <= ftx < cols - 2 and 2 <= fty < rows - 2:
                if on_path(ftx, fty) or (ftx, fty) in occupied:
                    continue
                if overlaps_house(ftx * TILE, fty * TILE):
                    continue
                px = ftx * TILE + random.randint(-2, 2)
                py = fty * TILE + random.randint(-2, 2)
                darken_grass_patch(bg, px + TILE // 2, py + TILE - 2,
                                   5, 3, alpha=70)
                draw_shadow(bg, px + TILE // 2 + 1, py + TILE - 2,
                            4, 2, alpha=70, blur=1.0)
                stamp(bg, SUNFLOWER, px, py)
                occupied.add((ftx, fty))
                planted += 1
                if planted >= n:
                    break
        if planted > 0:
            flowerbeds += 1

    # 6) Ground decorations — bushes, sunflowers, grass tufts (dense)
    decor = 0
    for ty in range(2, rows - 2):
        for tx in range(4, cols - 2):
            if on_path(tx, ty) or (tx, ty) in occupied:
                continue
            px, py = tx * TILE, ty * TILE
            if overlaps_house(px, py):
                continue
            roll = random.random()
            if roll < 0.04:    # bushes — way sparser (was 0.12)
                darken_grass_patch(bg, px + TILE // 2 + 1, py + TILE - 2,
                                   TILE // 2 + 3, 5, alpha=80)
                draw_shadow(bg, px + TILE // 2 + 2, py + TILE - 2,
                            7, 2, alpha=90, blur=1.4)
                # Only the big leafy bush — small bush had visible
                # rectangular silhouette at close zoom.
                stamp(bg, BUSH_BIG, px, py)
                occupied.add((tx, ty))
                decor += 1
            elif roll < 0.08:
                stamp(bg, GRASS_TUFT, px, py)

    # 7) Scattered boulders in clearings (1-2 per quadrant)
    for _ in range(8):
        tx = random.randint(6, cols - 6)
        ty = random.randint(4, rows - 5)
        if on_path(tx, ty) or near_path(tx, ty, 1) or (tx, ty) in occupied:
            continue
        if overlaps_house(tx * TILE, ty * TILE, 32, 32):
            continue
        px, py = tx * TILE, ty * TILE
        darken_grass_patch(bg, px + TILE, py + TILE * 2 - 2, TILE - 2, 4)
        draw_shadow(bg, px + TILE + 3, py + TILE * 2 - 2, TILE - 4, 3,
                    alpha=110, blur=1.5)
        stamp(bg, STONE_BIG, px, py)
        for ddy in range(2):
            for ddx in range(2):
                occupied.add((tx + ddx, ty + ddy))

    # 8) Fences disabled — isolated single fence segments next to houses
    # read as random floating wood structures, not yards. Re-enable only
    # when paired with shrubbery + a gate to form a real boundary.

    # Final touch — very mild contrast bump; saturation left alone so the
    # red-brown dirt path doesn't blow out to orange.
    from PIL import ImageEnhance
    bg = ImageEnhance.Contrast(bg).enhance(1.04)
    bg = ImageEnhance.Brightness(bg).enhance(0.95)

    # Apply a soft sandy tint over the path cells so they read as sandy
    # walking dirt, not lava-orange clay.
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for (tx, ty) in path_cells:
        od.rectangle(
            [tx * TILE, ty * TILE, tx * TILE + TILE, ty * TILE + TILE],
            fill=(220, 195, 140, 45),
        )
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=2.0))
    bg.alpha_composite(overlay)

    bg.save(OUT_PATH)
    print(f"wrote {OUT_PATH}  size={bg.size}  decor={decor}")


if __name__ == "__main__":
    main()
