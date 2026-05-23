#!/usr/bin/env python3
"""
Procedural placeholder pixel-art generator for 몽글마을.

Produces a tiny, cohesive cozy-farm tileset + a 4-directional character
spritesheet + a chicken sprite. Drop the outputs into assets/sprites/ and
the game will pick them up via the scene texture paths.

Run once:  python3 tools/gen_assets.py
Re-run any time the palette or sizes change.
"""

from __future__ import annotations

import os
import random
from PIL import Image, ImageDraw

random.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
os.makedirs(OUT_DIR, exist_ok=True)

# Cozy farm palette ----------------------------------------------------------
GRASS_LIGHT = (110, 168, 76)
GRASS_MID   = (84, 141, 62)
GRASS_DARK  = (62, 110, 50)
DIRT_LIGHT  = (199, 168, 117)
DIRT_DARK   = (142, 110, 71)
WATER_LIGHT = (95, 168, 211)
WATER_DARK  = (66, 132, 182)
ROOF_RED    = (174, 60, 50)
ROOF_RED_D  = (124, 40, 33)
ROOF_BROWN  = (120, 78, 50)
WOOD_LIGHT  = (171, 117, 79)
WOOD_DARK   = (110, 70, 47)
WINDOW      = (245, 220, 130)
DOOR        = (90, 50, 30)
LEAF_LIGHT  = (90, 160, 70)
LEAF_DARK   = (50, 110, 55)
TRUNK       = (90, 60, 40)
SKIN        = (244, 211, 168)
HAIR        = (90, 55, 33)
SHIRT       = (210, 90, 80)
PANTS       = (60, 75, 130)
SHOE        = (45, 32, 28)
WHITE       = (245, 245, 240)
BLACK       = (28, 28, 32)
BEAK        = (235, 175, 60)
FLOWER_P    = (231, 120, 160)
FLOWER_Y    = (245, 220, 80)
FLOWER_W    = (240, 240, 240)


def save(img: Image.Image, name: str) -> None:
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print(f"  wrote {os.path.relpath(path)}")


def noise_fill(img: Image.Image, base, accents, density=0.12):
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            px[x, y] = base
    for _ in range(int(w * h * density)):
        x = random.randrange(w)
        y = random.randrange(h)
        px[x, y] = random.choice(accents)
    return img


# Tiles ----------------------------------------------------------------------
def grass_tile() -> Image.Image:
    img = Image.new("RGBA", (32, 32))
    noise_fill(img, GRASS_LIGHT, [GRASS_MID, GRASS_MID, GRASS_DARK], density=0.18)
    return img


def grass_tile_dark() -> Image.Image:
    img = Image.new("RGBA", (32, 32))
    noise_fill(img, GRASS_MID, [GRASS_DARK, GRASS_DARK, GRASS_LIGHT], density=0.22)
    return img


def path_tile() -> Image.Image:
    img = Image.new("RGBA", (32, 32))
    noise_fill(img, DIRT_LIGHT, [DIRT_DARK, DIRT_LIGHT, DIRT_DARK], density=0.18)
    return img


def water_tile() -> Image.Image:
    img = Image.new("RGBA", (32, 32))
    px = img.load()
    for y in range(32):
        for x in range(32):
            px[x, y] = WATER_LIGHT if (x + y) % 8 < 4 else WATER_DARK
    return img


# Decorations ----------------------------------------------------------------
def pine_tree() -> Image.Image:
    img = Image.new("RGBA", (48, 64))
    d = ImageDraw.Draw(img)
    # trunk
    d.rectangle([20, 50, 27, 63], fill=TRUNK)
    # 3-tier foliage triangles
    tiers = [
        (24, 6, 18),   # cx, cy, half-width
        (24, 22, 22),
        (24, 38, 23),
    ]
    for cx, cy, hw in tiers:
        for dy in range(16):
            w = int(hw * (1 - dy / 18))
            for dx in range(-w, w + 1):
                if 0 <= cx + dx < 48 and 0 <= cy + dy < 64:
                    img.putpixel(
                        (cx + dx, cy + dy),
                        LEAF_LIGHT if (dx + dy) % 3 else LEAF_DARK,
                    )
    return img


def oak_tree() -> Image.Image:
    img = Image.new("RGBA", (48, 56))
    d = ImageDraw.Draw(img)
    d.rectangle([21, 42, 26, 55], fill=TRUNK)
    # round canopy
    d.ellipse([4, 0, 44, 44], fill=LEAF_LIGHT)
    d.ellipse([8, 4, 40, 38], fill=LEAF_DARK)
    d.ellipse([14, 8, 32, 28], fill=LEAF_LIGHT)
    # dither shadows
    px = img.load()
    for y in range(56):
        for x in range(48):
            if px[x, y] == LEAF_LIGHT and (x + y) % 5 == 0:
                px[x, y] = LEAF_DARK
    return img


def bush() -> Image.Image:
    img = Image.new("RGBA", (24, 16))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 2, 22, 14], fill=LEAF_DARK)
    d.ellipse([3, 0, 18, 10], fill=LEAF_LIGHT)
    return img


def flower(color) -> Image.Image:
    img = Image.new("RGBA", (8, 8))
    px = img.load()
    px[3, 3] = FLOWER_Y
    for x, y in [(2, 3), (4, 3), (3, 2), (3, 4)]:
        px[x, y] = color
    px[3, 6] = GRASS_DARK
    px[3, 7] = GRASS_DARK
    return img


# Houses ---------------------------------------------------------------------
def house(roof, roof_dark) -> Image.Image:
    img = Image.new("RGBA", (96, 96))
    d = ImageDraw.Draw(img)
    # body
    d.rectangle([12, 48, 84, 88], fill=WOOD_LIGHT)
    # wood plank lines
    for y in range(52, 88, 6):
        d.line([(12, y), (84, y)], fill=WOOD_DARK)
    # roof — pitched (parallelogram-ish triangle)
    for y in range(0, 50):
        row_inset = int(y * 0.85)
        x0 = 6 + row_inset
        x1 = 90 - row_inset
        if x0 >= x1:
            break
        for x in range(x0, x1 + 1):
            img.putpixel((x, y), roof if (x + y) % 7 else roof_dark)
    # roof edge shadow
    for x in range(6, 91):
        if img.getpixel((x, 49))[3] > 0:
            img.putpixel((x, 49), roof_dark)
    # door
    d.rectangle([42, 68, 54, 88], fill=DOOR)
    d.rectangle([42, 68, 54, 70], fill=BLACK)
    # windows
    d.rectangle([22, 58, 32, 68], fill=WINDOW)
    d.rectangle([22, 58, 32, 68], outline=WOOD_DARK)
    d.rectangle([64, 58, 74, 68], fill=WINDOW)
    d.rectangle([64, 58, 74, 68], outline=WOOD_DARK)
    # chimney
    d.rectangle([72, 6, 80, 24], fill=ROOF_BROWN)
    return img


# Character spritesheet -----------------------------------------------------
# 4 rows (down, left, right, up) x 2 frames; each frame is 16x24 px.
def chief_sheet() -> Image.Image:
    frame_w, frame_h = 16, 24
    cols, rows = 2, 4
    sheet = Image.new("RGBA", (frame_w * cols, frame_h * rows))
    for r, direction in enumerate(["down", "left", "right", "up"]):
        for c in range(cols):
            f = _chief_frame(direction, step=c)
            sheet.paste(f, (c * frame_w, r * frame_h))
    return sheet


def _chief_frame(direction: str, step: int) -> Image.Image:
    img = Image.new("RGBA", (16, 24))
    d = ImageDraw.Draw(img)
    # hair / head
    d.rectangle([4, 2, 11, 8], fill=HAIR)
    d.rectangle([4, 5, 11, 10], fill=SKIN)
    # eyes
    if direction == "down":
        d.point((6, 7), fill=BLACK)
        d.point((9, 7), fill=BLACK)
    elif direction == "up":
        d.rectangle([4, 2, 11, 9], fill=HAIR)
    elif direction == "left":
        d.point((5, 7), fill=BLACK)
    elif direction == "right":
        d.point((10, 7), fill=BLACK)
    # body shirt
    d.rectangle([4, 10, 11, 16], fill=SHIRT)
    # arms
    if direction in ("down", "up"):
        d.rectangle([3, 11, 4, 15], fill=SHIRT)
        d.rectangle([11, 11, 12, 15], fill=SHIRT)
    # pants
    d.rectangle([4, 16, 11, 20], fill=PANTS)
    # legs (animated)
    if step == 0:
        d.rectangle([5, 20, 7, 23], fill=SHOE)
        d.rectangle([8, 20, 10, 23], fill=SHOE)
    else:
        d.rectangle([4, 20, 6, 23], fill=SHOE)
        d.rectangle([9, 20, 11, 23], fill=SHOE)
    return img


def chicken_sheet() -> Image.Image:
    img = Image.new("RGBA", (32, 16))
    for c in range(2):
        f = Image.new("RGBA", (16, 16))
        d = ImageDraw.Draw(f)
        # body
        d.ellipse([3, 5, 13, 13], fill=WHITE)
        # head
        d.ellipse([8, 2, 14, 8], fill=WHITE)
        # eye + beak
        d.point((12, 4), fill=BLACK)
        d.rectangle([13, 5, 15, 6], fill=BEAK)
        # comb
        d.point((11, 1), fill=ROOF_RED)
        d.point((12, 1), fill=ROOF_RED)
        # legs
        leg_offset = c
        d.line([(6, 13), (6 + leg_offset, 15)], fill=BEAK)
        d.line([(10, 13), (10 - leg_offset, 15)], fill=BEAK)
        img.paste(f, (c * 16, 0))
    return img


# Full prebuilt village background ------------------------------------------
def village_background(grass: Image.Image, dark: Image.Image,
                       path: Image.Image, water: Image.Image,
                       pine: Image.Image, oak: Image.Image,
                       bush_img: Image.Image,
                       f_pink: Image.Image, f_yellow: Image.Image,
                       f_white: Image.Image,
                       house_red: Image.Image, house_brown: Image.Image,
                       w_tiles=60, h_tiles=34, tile=32) -> Image.Image:
    W = w_tiles * tile
    H = h_tiles * tile
    bg = Image.new("RGBA", (W, H))

    # base grass
    for ty in range(h_tiles):
        for tx in range(w_tiles):
            t = grass if random.random() > 0.18 else dark
            bg.paste(t, (tx * tile, ty * tile))

    # water river along left edge
    for ty in range(h_tiles):
        for tx in range(0, 3):
            wobble = int((ty % 5 == 0))
            bg.paste(water, ((tx + wobble) * tile, ty * tile))

    # cross-shaped dirt paths
    cx = w_tiles // 2
    cy = h_tiles // 2
    for ty in range(h_tiles):
        for dx in range(-2, 3):
            bg.paste(path, ((cx + dx) * tile, ty * tile))
    for tx in range(3, w_tiles):
        for dy in range(-2, 3):
            bg.paste(path, (tx * tile, (cy + dy) * tile))

    # forest border (pines on outer 4 rows/cols)
    def is_path_tile(tx, ty):
        return (abs(tx - cx) <= 2) or (abs(ty - cy) <= 2 and tx >= 3)

    for ty in range(h_tiles):
        for tx in range(w_tiles):
            if tx < 3:  # water area
                continue
            on_edge = (ty < 3 or ty >= h_tiles - 3 or tx >= w_tiles - 3)
            if on_edge and not is_path_tile(tx, ty) and random.random() < 0.55:
                tree = pine if random.random() < 0.7 else oak
                bg.alpha_composite(tree, (tx * tile - 8, ty * tile - 16))

    # scatter bushes + flowers in non-path areas
    for _ in range(120):
        tx = random.randrange(4, w_tiles - 2)
        ty = random.randrange(3, h_tiles - 3)
        if is_path_tile(tx, ty):
            continue
        kind = random.random()
        x = tx * tile + random.randrange(0, 16)
        y = ty * tile + random.randrange(0, 16)
        if kind < 0.25:
            bg.alpha_composite(bush_img, (x, y))
        elif kind < 0.5:
            bg.alpha_composite(f_pink, (x, y))
        elif kind < 0.75:
            bg.alpha_composite(f_yellow, (x, y))
        else:
            bg.alpha_composite(f_white, (x, y))

    # place a few houses in 4 quadrants
    placements = [
        (cx - 12, cy - 9, house_red),
        (cx + 6,  cy - 9, house_brown),
        (cx - 14, cy + 4, house_red),
        (cx + 8,  cy + 4, house_brown),
        (cx + 14, cy + 5, house_red),
    ]
    for (tx, ty, hs) in placements:
        bg.alpha_composite(hs, (tx * tile, ty * tile))

    return bg


def main() -> None:
    print("Generating placeholder pixel-art assets...")
    grass = grass_tile()
    dark = grass_tile_dark()
    path = path_tile()
    water = water_tile()
    pine = pine_tree()
    oak = oak_tree()
    bush_img = bush()
    f_pink = flower(FLOWER_P)
    f_yellow = flower(FLOWER_Y)
    f_white = flower(FLOWER_W)
    house_red = house(ROOF_RED, ROOF_RED_D)
    house_brown = house(ROOF_BROWN, WOOD_DARK)
    chief = chief_sheet()
    chicken = chicken_sheet()

    save(grass, "tile_grass.png")
    save(dark, "tile_grass_dark.png")
    save(path, "tile_path.png")
    save(water, "tile_water.png")
    save(pine, "tree_pine.png")
    save(oak, "tree_oak.png")
    save(bush_img, "bush.png")
    save(f_pink, "flower_pink.png")
    save(f_yellow, "flower_yellow.png")
    save(f_white, "flower_white.png")
    save(house_red, "house_red.png")
    save(house_brown, "house_brown.png")
    save(chief, "chief_sheet.png")
    save(chicken, "chicken_sheet.png")

    print("\nBuilding prebuilt village background...")
    bg = village_background(
        grass, dark, path, water, pine, oak,
        bush_img, f_pink, f_yellow, f_white,
        house_red, house_brown,
    )
    save(bg, "village_background.png")
    print(f"  background size: {bg.size}")
    print("\nDone.")


if __name__ == "__main__":
    main()
