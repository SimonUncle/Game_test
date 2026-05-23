#!/usr/bin/env python3
"""
Compose a village PNG from the Sparklin Labs Ninja Adventure tileset (CC0).

Tile coords were identified by overlaying a numbered grid on the tileset
and visually picking which tile fits each role. They are NOT part of any
formal spec — they're empirical for this specific sheet.
"""

from __future__ import annotations

import os
import random
from PIL import Image

random.seed(11)

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


# Identified coordinates ----------------------------------------------------
GRASS_TILES = [(11, 16), (12, 16), (13, 16)]
DIRT_TILE = (21, 16)
WATER_TILE = (20, 8)

HOUSES = [
    chunk(0,  0, 5, 3),    # orange roof, big
    chunk(5,  0, 5, 3),    # light roof, big
    chunk(10, 0, 5, 3),    # orange roof variant
    chunk(15, 0, 5, 3),    # red brick roof, big
]

TREES = [
    chunk(4,  10, 2, 2),   # round leafy
    chunk(8,  10, 2, 2),   # darker round
    chunk(4,  10, 2, 2),
    chunk(8,  10, 2, 2),
]

BUSH_TILE  = tile(12, 11)
ROCK_TILE  = tile(14, 10)
FLOWER_TILES = [tile(2, 9), tile(3, 9)]


def stamp(canvas: Image.Image, img: Image.Image, x_px: int, y_px: int) -> None:
    canvas.alpha_composite(img, (x_px, y_px))


def main() -> None:
    cols, rows = 80, 48      # 1280x768 world
    W, H = cols * TILE, rows * TILE

    bg = Image.new("RGBA", (W, H), (90, 140, 70, 255))

    grass = [tile(*t) for t in GRASS_TILES]
    dirt = tile(*DIRT_TILE)
    water = tile(*WATER_TILE)

    # base grass
    for ty in range(rows):
        for tx in range(cols):
            bg.paste(random.choice(grass), (tx * TILE, ty * TILE))

    # water river on the far left (3-4 tiles wide, wavy)
    for ty in range(rows):
        width = 3 + (1 if ty % 5 == 0 else 0)
        for tx in range(width):
            bg.paste(water, (tx * TILE, ty * TILE))

    # cross-shaped dirt paths centered in the playable area
    cx, cy = cols // 2, rows // 2

    def on_path(tx: int, ty: int) -> bool:
        if abs(tx - cx) <= 2:
            return True
        if abs(ty - cy) <= 2 and tx >= 5:
            return True
        return False

    for ty in range(rows):
        for tx in range(cols):
            if tx < 5:
                continue
            if on_path(tx, ty):
                bg.paste(dirt, (tx * TILE, ty * TILE))

    # houses in the 4 quadrants (tile-coords of top-left)
    placements = [
        (HOUSES[0], 10, 8),
        (HOUSES[1], 22, 6),
        (HOUSES[2], 50, 7),
        (HOUSES[3], 64, 9),
        (HOUSES[3], 10, 28),
        (HOUSES[1], 26, 30),
        (HOUSES[0], 50, 28),
        (HOUSES[2], 65, 30),
    ]
    house_rects = []
    for (img, tx, ty) in placements:
        px, py = tx * TILE, ty * TILE
        stamp(bg, img, px, py)
        house_rects.append((px, py, img.size[0], img.size[1]))

    def overlaps_house(px, py, w=16, h=16) -> bool:
        for (hx, hy, hw, hh) in house_rects:
            if px + w > hx and px < hx + hw and py + h > hy and py < hy + hh:
                return True
        return False

    # forest: dense lush border (3 rings deep), some interior clumps
    border_depth = 4
    for ty in range(rows):
        for tx in range(cols):
            if tx < 5 or on_path(tx, ty):
                continue
            dist_from_edge = min(ty, rows - 1 - ty, cols - 1 - tx)
            if dist_from_edge < border_depth:
                density = 0.90 - (dist_from_edge * 0.18)
            else:
                density = 0.05
            if random.random() < density:
                tree = random.choice(TREES)
                px = tx * TILE + random.randint(-4, 4)
                py = ty * TILE - TILE + random.randint(-2, 2)
                if not overlaps_house(px, py, *tree.size):
                    stamp(bg, tree, max(0, px), max(0, py))

    # bushes / rocks / flowers scattered in grass
    for _ in range(280):
        tx = random.randint(6, cols - 4)
        ty = random.randint(3, rows - 3)
        if on_path(tx, ty):
            continue
        px = tx * TILE + random.randint(0, 6)
        py = ty * TILE + random.randint(0, 6)
        if overlaps_house(px, py):
            continue
        r = random.random()
        if r < 0.45:
            stamp(bg, BUSH_TILE, px, py)
        elif r < 0.65:
            stamp(bg, ROCK_TILE, px, py)
        else:
            stamp(bg, random.choice(FLOWER_TILES), px, py)

    bg.save(OUT_PATH)
    print(f"wrote {OUT_PATH}  size={bg.size}")


if __name__ == "__main__":
    main()
