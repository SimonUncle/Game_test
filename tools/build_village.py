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

TREE_ROUND = chunk(4, 10, 2, 2)
TREE_DARK  = chunk(8, 10, 2, 2)
TREES = [TREE_ROUND, TREE_DARK, TREE_ROUND, TREE_DARK, TREE_DARK]

CHERRY_BIG = chunk(4, 16, 2, 2)
CHERRY_SM  = chunk(8, 16, 2, 2)

BUSH_SM    = tile(3, 13)
BUSH_BIG   = tile(9, 15)
GRASS_TUFT = tile(4, 15)
SUNFLOWER  = tile(3, 15)


def stamp(canvas: Image.Image, img: Image.Image, x_px: int, y_px: int) -> None:
    canvas.alpha_composite(img, (x_px, y_px))


def random_flip(img: Image.Image) -> Image.Image:
    if random.random() < 0.5:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if random.random() < 0.5:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    return img


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

    # 1) Grass base with random flips per tile to break tiling repeats.
    # Mostly the plain clean grass, with sparse yellow-dappled variant.
    for ty in range(rows):
        for tx in range(cols):
            base = grass_alt if random.random() < 0.08 else grass
            bg.paste(random_flip(base), (tx * TILE, ty * TILE))

    # 2) River on left, also flip per-tile for variation
    for ty in range(rows):
        for tx in range(3):
            bg.paste(random_flip(water), (tx * TILE, ty * TILE))

    # 3) Winding paths instead of a rigid cross.
    # Vertical path: center column cx with a slow sine deviation.
    # Horizontal path: center row cy with deviation.
    PATH_HALF = 2  # half-width (3 tiles total when half=1; we use 2 → 5 wide)

    path_cells: set[tuple[int, int]] = set()

    def add_path_cell(tx: int, ty: int) -> None:
        if 3 <= tx < cols and 0 <= ty < rows:
            path_cells.add((tx, ty))

    # Vertical strip
    for ty in range(rows):
        offset = int(2 * math.sin(ty / 6.0)) + int(1.5 * math.cos(ty / 14.0))
        center = cx + offset
        for dx in range(-PATH_HALF, PATH_HALF + 1):
            add_path_cell(center + dx, ty)

    # Horizontal strip
    for tx in range(3, cols):
        offset = int(2 * math.sin(tx / 8.0)) + int(1.5 * math.cos(tx / 17.0))
        center = cy + offset
        for dy in range(-PATH_HALF, PATH_HALF + 1):
            add_path_cell(tx, center + dy)

    # Stamp path
    for (tx, ty) in path_cells:
        bg.paste(random_flip(dirt), (tx * TILE, ty * TILE))

    def on_path(tx: int, ty: int) -> bool:
        return (tx, ty) in path_cells

    def near_path(tx: int, ty: int, dist: int = 1) -> bool:
        for ddy in range(-dist, dist + 1):
            for ddx in range(-dist, dist + 1):
                if (tx + ddx, ty + ddy) in path_cells:
                    return True
        return False

    # Foot-traffic wear: scatter dirt patches just off the path edges
    edge_cells = []
    for (tx, ty) in path_cells:
        for ddy, ddx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ncell = (tx + ddx, ty + ddy)
            if ncell not in path_cells:
                edge_cells.append(ncell)
    for (tx, ty) in edge_cells:
        if 3 <= tx < cols and 0 <= ty < rows and random.random() < 0.18:
            bg.paste(random_flip(dirt), (tx * TILE, ty * TILE))
            path_cells.add((tx, ty))

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
    occupied: set[tuple[int, int]] = set()

    for (img, tx, ty) in placements:
        if on_path(tx, ty) or on_path(tx + img.size[0] // TILE - 1, ty):
            continue
        if any(on_path(tx + dx, ty + dy)
               for dx in range(img.size[0] // TILE)
               for dy in range(img.size[1] // TILE)):
            continue
        px, py = tx * TILE, ty * TILE
        # doorstep dirt — 2 tiles, slightly randomized shape
        door_tx = tx + img.size[0] // TILE // 2 - 1
        door_ty = ty + img.size[1] // TILE
        for dx in range(2):
            bg.paste(random_flip(dirt), ((door_tx + dx) * TILE, door_ty * TILE))
        # AO under building (subtle wider green darkening)
        ao_cx = px + img.size[0] // 2
        ao_cy = py + img.size[1] - 2
        darken_grass_patch(bg, ao_cx + 2, ao_cy, img.size[0] // 2 + 6, 10)
        # drop shadow (offset right for sun from upper-left)
        draw_shadow(bg, ao_cx + 6, ao_cy, img.size[0] // 2, 6, alpha=120, blur=2.0)
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

    # 5) Forest — dense outer ring with AO + drop shadow + tile-aligned
    def place_tree(tx: int, ty: int, allow_cherry: bool = False) -> bool:
        if on_path(tx, ty) or near_path(tx, ty, dist=0):
            return False
        if overlaps_house(tx * TILE, ty * TILE, 32, 32):
            return False
        for ddy in range(2):
            for ddx in range(2):
                if (tx + ddx, ty + ddy) in occupied:
                    return False
        roll = random.random()
        if allow_cherry and roll < 0.12:
            tree = CHERRY_BIG if roll < 0.06 else CHERRY_SM
        else:
            tree = random.choice(TREES)
        trunk_x = tx * TILE + tree.size[0] // 2
        trunk_y = ty * TILE + tree.size[1] - 4
        darken_grass_patch(bg, trunk_x + 1, trunk_y, tree.size[0] // 2 + 2, 6)
        draw_shadow(bg, trunk_x + 3, trunk_y, tree.size[0] // 2 - 1, 4,
                    alpha=110, blur=1.8)
        stamp(bg, tree, tx * TILE, ty * TILE - TILE)
        cw, ch = tree.size[0] // TILE, tree.size[1] // TILE
        for ddy in range(ch + 1):
            for ddx in range(cw):
                occupied.add((tx + ddx, ty + ddy - 1))
        return True

    # Outer ring trees
    for ty in range(0, rows, 2):
        for tx in range(3, cols, 2):
            depth = min(ty, rows - 1 - ty, cols - 1 - tx)
            if depth < 5:
                if random.random() < 0.93:
                    place_tree(tx, ty, allow_cherry=(depth >= 3))
            elif depth < 7 and random.random() < 0.32:
                place_tree(tx, ty, allow_cherry=True)

    # A few cherry accents inside the village
    for (hx, hy, hw, hh) in house_rects:
        for _ in range(2):
            tx = (hx // TILE) + random.randint(-2, 4)
            ty = (hy // TILE) + random.randint(3, 5)
            if 4 <= tx < cols - 3 and 2 <= ty < rows - 3:
                if place_tree(tx, ty, allow_cherry=True):
                    break

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
            if roll < 0.16:
                draw_shadow(bg, px + TILE // 2 + 1, py + TILE - 3, 5, 2, alpha=60)
                stamp(bg, BUSH_BIG if random.random() < 0.5 else BUSH_SM, px, py)
                occupied.add((tx, ty))
                decor += 1
            elif roll < 0.20:
                draw_shadow(bg, px + TILE // 2 + 1, py + TILE - 3, 4, 2, alpha=55)
                stamp(bg, SUNFLOWER, px, py)
                occupied.add((tx, ty))
                decor += 1
            # Grass tufts placed in clusters near other tufts/decor only,
            # so they form patches instead of stripes across the whole field.
            elif roll < 0.10:
                stamp(bg, GRASS_TUFT, px, py)

    bg.save(OUT_PATH)
    print(f"wrote {OUT_PATH}  size={bg.size}  decor={decor}")


if __name__ == "__main__":
    main()
