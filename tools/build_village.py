#!/usr/bin/env python3
"""
Compose the village PNG from the Sparklin Labs Ninja Adventure tileset (CC0).

Lessons from the previous pass:
 - Houses in this tileset are 4 wide x 3 tall, not 5x3. Cropping 5x3
   bled the start of the neighbor house in and made everything look
   half-finished.
 - Mixing multiple grass tile variants randomly makes the ground look
   patchy. Stardew-style tilesets use ONE base grass with sparse
   decoration sprites on top — we follow that here.
 - Trees stamped with random sub-tile offsets create a noisy grid.
   We keep them tile-aligned.
"""

from __future__ import annotations

import os
import random
from PIL import Image

random.seed(13)

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


# Verified after grid inspection -------------------------------------------
GRASS_BASE = (12, 16)           # ONE consistent grass tile
DIRT       = (21, 16)
WATER      = (20, 8)

HOUSES = [
    chunk(0,  0, 4, 3),         # 64x48  orange roof, 3 openings
    chunk(4,  0, 4, 3),         # beige roof, 1 door
    chunk(8,  0, 4, 3),         # orange roof variant
    chunk(12, 0, 4, 3),         # red brick pagoda
]

TREE_ROUND = chunk(4, 10, 2, 2)
TREE_DARK  = chunk(8, 10, 2, 2)
TREES = [TREE_ROUND, TREE_DARK]

BUSH       = tile(3, 13)        # small green bush on dirt patch


def stamp(canvas: Image.Image, img: Image.Image, x_px: int, y_px: int) -> None:
    canvas.alpha_composite(img, (x_px, y_px))


def main() -> None:
    cols, rows = 80, 48
    W, H = cols * TILE, rows * TILE
    cx, cy = cols // 2, rows // 2

    bg = Image.new("RGBA", (W, H), (90, 140, 70, 255))
    grass = tile(*GRASS_BASE)
    dirt = tile(*DIRT)
    water = tile(*WATER)

    # 1) Single grass base everywhere
    for ty in range(rows):
        for tx in range(cols):
            bg.paste(grass, (tx * TILE, ty * TILE))

    # 2) River on the far left (3 tiles wide)
    for ty in range(rows):
        for tx in range(3):
            bg.paste(water, (tx * TILE, ty * TILE))

    # 3) Cross dirt paths
    def on_path(tx: int, ty: int) -> bool:
        if tx < 3:
            return False
        if abs(tx - cx) <= 2:
            return True
        if abs(ty - cy) <= 2 and tx >= 3:
            return True
        return False

    for ty in range(rows):
        for tx in range(cols):
            if on_path(tx, ty):
                bg.paste(dirt, (tx * TILE, ty * TILE))

    # 4) Houses (tile coords of top-left). With doorstep dirt in front.
    placements = [
        (HOUSES[0], 8,  8),
        (HOUSES[1], 18, 7),
        (HOUSES[2], 48, 7),
        (HOUSES[3], 64, 8),
        (HOUSES[3], 8,  28),
        (HOUSES[0], 18, 30),
        (HOUSES[1], 48, 28),
        (HOUSES[2], 64, 30),
    ]
    house_rects = []
    for (img, tx, ty) in placements:
        px, py = tx * TILE, ty * TILE
        # doorstep: a single dirt tile right under the door
        door_tx = tx + img.size[0] // TILE // 2
        door_ty = ty + img.size[1] // TILE
        bg.paste(dirt, (door_tx * TILE, door_ty * TILE))
        # then the house on top
        stamp(bg, img, px, py)
        house_rects.append((px, py, img.size[0], img.size[1]))

    def overlaps_house(px, py, w=16, h=16) -> bool:
        for (hx, hy, hw, hh) in house_rects:
            if px + w > hx and px < hx + hw and py + h > hy and py < hy + hh:
                return True
        return False

    def near_path(tx: int, ty: int) -> bool:
        for ddy in range(-1, 2):
            for ddx in range(-1, 2):
                if on_path(tx + ddx, ty + ddy):
                    return True
        return False

    # 5) Forest border — dense 4-tile-deep ring of trees, tile-aligned.
    # We sample on a coarser grid (every 2 tiles) so trees don't overlap
    # awkwardly. Each tree is 2x2 tiles centered on the sample point.
    occupied = set()  # (tx, ty) cells where a tree already sits

    def place_tree(tx: int, ty: int) -> bool:
        if on_path(tx, ty) or near_path(tx, ty):
            return False
        if overlaps_house(tx * TILE, ty * TILE, 32, 32):
            return False
        for ddy in range(2):
            for ddx in range(2):
                if (tx + ddx, ty + ddy) in occupied:
                    return False
        tree = random.choice(TREES)
        stamp(bg, tree, tx * TILE, ty * TILE - TILE)
        for ddy in range(2):
            for ddx in range(2):
                occupied.add((tx + ddx, ty + ddy))
        return True

    # Outer ring (dense)
    for ty in range(0, rows, 2):
        for tx in range(3, cols, 2):
            depth = min(ty, rows - 1 - ty, cols - 1 - tx)
            if depth < 4:
                if random.random() < 0.95:
                    place_tree(tx, ty)
            elif depth < 6 and random.random() < 0.35:
                place_tree(tx, ty)

    # Interior accent trees (very sparse)
    for _ in range(18):
        tx = random.randint(6, cols - 6)
        ty = random.randint(6, rows - 6)
        place_tree(tx, ty)

    # 6) Sparse bushes in grass for visual interest. Avoid overcrowding —
    # the original reference is mostly clean grass with a few accents.
    for _ in range(50):
        tx = random.randint(4, cols - 3)
        ty = random.randint(2, rows - 3)
        if on_path(tx, ty) or (tx, ty) in occupied:
            continue
        px, py = tx * TILE, ty * TILE
        if overlaps_house(px, py):
            continue
        stamp(bg, BUSH, px, py)

    bg.save(OUT_PATH)
    print(f"wrote {OUT_PATH}  size={bg.size}")


if __name__ == "__main__":
    main()
