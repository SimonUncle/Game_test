#!/usr/bin/env python3
"""
Compose a dense, shadowed village PNG from the Sparklin Labs Ninja Adventure
tileset (CC0). Aims for Stardew Valley-style density: drop shadows under
every standing object, layered foliage, multiple house variants, cherry
blossom accents, sunflowers, fences, stones.
"""

from __future__ import annotations

import os
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(17)

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


# Verified coordinates ------------------------------------------------------
GRASS      = (12, 16)
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

# Cherry-blossom (pink/peach) trees — full tree at rows 16-17
CHERRY_BIG = chunk(4, 16, 2, 2)
CHERRY_SM  = chunk(8, 16, 2, 2)

BUSH_SM    = tile(3, 13)        # small green bush
BUSH_BIG   = tile(9, 15)        # big leafy bush
GRASS_TUFT = tile(4, 15)        # tiny green leaves
SUNFLOWER  = tile(3, 15)        # proper sunflower


def stamp(canvas: Image.Image, img: Image.Image, x_px: int, y_px: int) -> None:
    canvas.alpha_composite(img, (x_px, y_px))


def draw_shadow(canvas: Image.Image, cx: int, cy: int, rx: int, ry: int,
                alpha: int = 90) -> None:
    """Soft elliptical drop shadow centered at (cx, cy)."""
    pad = 4
    layer = Image.new("RGBA", (rx * 2 + pad * 2, ry * 2 + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([pad, pad, pad + rx * 2, pad + ry * 2], fill=(0, 0, 0, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=1.5))
    canvas.alpha_composite(layer, (cx - rx - pad, cy - ry - pad))


def main() -> None:
    cols, rows = 80, 48
    W, H = cols * TILE, rows * TILE
    cx, cy = cols // 2, rows // 2

    bg = Image.new("RGBA", (W, H), (90, 140, 70, 255))
    grass = tile(*GRASS)
    dirt = tile(*DIRT)
    water = tile(*WATER)

    # 1) Single grass base everywhere
    for ty in range(rows):
        for tx in range(cols):
            bg.paste(grass, (tx * TILE, ty * TILE))

    # 2) Wider river on the left
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

    # Soften grass<->path borders by sprinkling grass tufts at the edges.
    path_edge_cells = []
    for ty in range(rows):
        for tx in range(cols):
            if on_path(tx, ty):
                continue
            for ddy, ddx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if on_path(tx + ddx, ty + ddy):
                    path_edge_cells.append((tx, ty))
                    break
    for (tx, ty) in path_edge_cells:
        if random.random() < 0.6:
            stamp(bg, GRASS_TUFT, tx * TILE, ty * TILE)

    # 4) Houses — 8 placements, mixed types. Drop shadows first, then sprites.
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
        px, py = tx * TILE, ty * TILE
        # doorstep dirt
        door_tx = tx + img.size[0] // TILE // 2 - 1
        door_ty = ty + img.size[1] // TILE
        for dx in range(2):
            bg.paste(dirt, ((door_tx + dx) * TILE, door_ty * TILE))
        # drop shadow under the building footprint
        bottom_y = py + img.size[1] - 4
        draw_shadow(bg, px + img.size[0] // 2 + 4, bottom_y, img.size[0] // 2, 8, alpha=110)
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

    def near_path(tx: int, ty: int, dist: int = 1) -> bool:
        for ddy in range(-dist, dist + 1):
            for ddx in range(-dist, dist + 1):
                if on_path(tx + ddx, ty + ddy):
                    return True
        return False

    # 5) Forest: 5-tile-deep DENSE outer ring, scattered interior accents,
    #    with cherry blossom accents for color contrast.
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
        # drop shadow at trunk base
        trunk_x = tx * TILE + tree.size[0] // 2
        trunk_y = ty * TILE + tree.size[1] - 4
        draw_shadow(bg, trunk_x, trunk_y, tree.size[0] // 2 - 2, 5, alpha=95)
        stamp(bg, tree, tx * TILE, ty * TILE - TILE)
        cw, ch = tree.size[0] // TILE, tree.size[1] // TILE
        for ddy in range(ch + 1):
            for ddx in range(cw):
                occupied.add((tx + ddx, ty + ddy - 1))
        return True

    # Outer ring — very dense (90%+ fill), 5 tiles deep
    for ty in range(0, rows, 2):
        for tx in range(3, cols, 2):
            depth = min(ty, rows - 1 - ty, cols - 1 - tx)
            if depth < 5:
                if random.random() < 0.92:
                    place_tree(tx, ty, allow_cherry=(depth >= 3))
            elif depth < 7 and random.random() < 0.30:
                place_tree(tx, ty, allow_cherry=True)

    # Some cherry tree accents inside the village near houses
    for (hx, hy, hw, hh) in house_rects:
        # try one cherry near each house
        for _ in range(3):
            tx = (hx // TILE) + random.randint(-3, 4)
            ty = (hy // TILE) + random.randint(2, 5)
            if 4 <= tx < cols - 3 and 2 <= ty < rows - 3:
                if place_tree(tx, ty, allow_cherry=True):
                    break

    # 6) Dense ground decorations — bushes, sunflowers, grass tufts.
    # Use Poisson-ish sampling on a 1-tile grid with high density.
    decor_count = 0
    for ty in range(2, rows - 2):
        for tx in range(4, cols - 2):
            if on_path(tx, ty) or near_path(tx, ty, dist=0):
                continue
            if (tx, ty) in occupied:
                continue
            px, py = tx * TILE, ty * TILE
            if overlaps_house(px, py):
                continue
            roll = random.random()
            if roll < 0.18:
                # bush — small shadow
                draw_shadow(bg, px + TILE // 2 + 1, py + TILE - 3, 6, 3, alpha=70)
                stamp(bg, BUSH_BIG if random.random() < 0.5 else BUSH_SM, px, py)
                occupied.add((tx, ty))
                decor_count += 1
            elif roll < 0.22:
                draw_shadow(bg, px + TILE // 2 + 1, py + TILE - 3, 5, 3, alpha=70)
                stamp(bg, SUNFLOWER, px, py)
                occupied.add((tx, ty))
                decor_count += 1
            elif roll < 0.35:
                stamp(bg, GRASS_TUFT, px, py)

    bg.save(OUT_PATH)
    print(f"wrote {OUT_PATH}  size={bg.size}  decor={decor_count}")


if __name__ == "__main__":
    main()
