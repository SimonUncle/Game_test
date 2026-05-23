---
name: tile-check
description: |
  Inspect specific tile coordinates in the Sparklin ninja tileset and
  show what they actually contain. Use this BEFORE registering any new
  tile coordinate in build_village.py. Catches "I thought this was a
  bush but it's actually a tree stump" mistakes that wasted hours of
  this project.
allowed-tools: Bash, Read, SendUserFile
---

# Tile checker

Crops the requested 16×16 tile (or N×M chunk) from
`assets/sparklin/ninja_tileset.png`, scales it 8× with nearest-neighbor,
saves a preview PNG, and shows it. NEVER add a tile coordinate to
`build_village.py` without running this first.

## Usage

User invokes with one or more coords:

```
/tile-check 3,13
/tile-check 12,16 13,16 14,16     # compare 3 candidates
/tile-check chunk:4,16,2,2         # 2×2 chunk
```

## What to do

1. Parse coords from `$args`. Format options:
   - `c,r` → single 16×16 tile at column c, row r
   - `chunk:c,r,w,h` → multi-tile chunk

2. For each coord, run:

```python
from PIL import Image
ts = Image.open("assets/sparklin/ninja_tileset.png").convert("RGBA")
TILE = 16
c, r, w, h = <parsed>
im = ts.crop((c*TILE, r*TILE, (c+w)*TILE, (r+h)*TILE))
im.resize((im.size[0]*8, im.size[1]*8), Image.NEAREST).save(f"/tmp/tile_{c}_{r}.png")
```

3. Read each output PNG with `Read` and show what each is.

4. For each tile, explicitly state what's visible. Don't guess names —
   describe what you see ("small green plant with brown base",
   not "it's a bush").

5. If user wanted to register this in build_village.py, only proceed
   after they confirm the visual matches their intent.

## Common traps this skill catches

- (12, 11) looks like green from a distance but is actually a tree
  stump
- (2, 9) and (3, 9) look orange but are carrot icons, not flowers
- (3, 16) looks like a flower but is a peach food item
- (12, 16) appears to be plain grass but has a 1-pixel black left
  edge that becomes a vertical stripe when tiled
- House chunks: each house is 4×3, not 5×3 — cropping 5×3 includes
  part of the next building
