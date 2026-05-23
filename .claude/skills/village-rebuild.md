---
name: village-rebuild
description: |
  One-shot rebuild loop: regenerate village_background.png from
  build_village.py, re-import in Godot, capture a fresh screenshot,
  and surface the result. Use this every time build_village.py
  changes. Replaces the 4-command sequence we kept retyping.
allowed-tools: Bash, Read, SendUserFile
---

# Village rebuild loop

Runs the complete validate-after-change loop in ~30 seconds. Use after
ANY edit to `tools/build_village.py` so visual regressions are caught
immediately.

## Steps (run in this order; stop on the first failure)

```bash
# 1. Regenerate the composed PNG (~5s)
python3 tools/build_village.py

# 2. Re-import Godot resources (only needed if PNG was overwritten, ~10s)
godot --headless --import --path . 2>&1 | tail -3

# 3. Headless validate — exit 0 + no error lines = clean
godot --headless --verbose --path . --quit-after 60 scenes/main.tscn 2>&1 \
  | grep -iE "(error|warning|fail)" \
  | grep -v ALSA | grep -v vsync | head -20

# 4. Fresh screenshot
rm -f "/root/.local/share/godot/app_userdata/몽글마을 (Mongle Village)/screenshot.png"
xvfb-run -a -s "-screen 0 1920x1080x24" \
  godot --path . --resolution 1920x1080 tools/screenshot.tscn 2>&1 \
  | grep -E "(saved|Error)" | head -3
cp "/root/.local/share/godot/app_userdata/몽글마을 (Mongle Village)/screenshot.png" /tmp/last_build.png
```

## Then

1. Read the screenshot and assess: did the change land? Any new artifacts?
2. Optionally surface to user with `SendUserFile` if they should see it.
3. If broken: diagnose with a SINGLE specific question ("which area
   looks wrong?") rather than guessing a fix.

## What to report

- ✅ on success, with one-line summary of what changed visually
- ❌ on parse errors or scripting errors (don't continue past these)
- ⚠️ on warnings that are non-fatal (notably, ignore ALSA + vsync;
  they're environment quirks, not project bugs)
