# 몽글마을 (Mongle Village)

> A cozy pixel-art village simulation with a built-in Pomodoro focus timer,
> daily todos, and resident notifications. Stardew-Valley-style art direction;
> productivity at heart.

Built with **[Godot 4.3+](https://godotengine.org/)** (GL Compatibility renderer,
runs on low-spec laptops and the web).

---

## 🚀 Quick start

1. **Install Godot 4.3 or newer** — download the *Standard* build from
   https://godotengine.org/download. No installation required; it's a single
   executable.
2. Open Godot. On the Project Manager screen click **Import**, navigate to
   this folder, select `project.godot`, and click **Import & Edit**.
3. Press **F5** (or the ▶ button top-right) to run. Godot will ask you to
   pick a main scene the very first time — choose `scenes/main.tscn`.

That's it. Everything works out of the box: timer, todos, notifications,
top nav, autosave.

---

## 🎮 Controls

| Key | Action |
|---|---|
| `W` `A` `S` `D` / Arrows | Move the chief around the village |
| `Space` | Interact (reserved for future NPCs) |
| `Esc` | Start/Pause focus timer |
| Click `+` on the date card | Focus the todo input |
| Click `▶ START` | Begin a 25-minute focus cycle |

---

## 🧱 Project structure

```
.
├── project.godot              # Engine config, autoloads, input map
├── icon.svg                   # Window/taskbar icon (placeholder)
├── scenes/
│   ├── main.tscn              # The village + UI layer
│   ├── player.tscn            # CharacterBody2D with 8-dir movement
│   └── ui/
│       ├── top_nav.tscn       # TOWN INFO / RESIDENTS / SETTINGS / LOGIN
│       ├── pomodoro_panel.tscn
│       ├── date_panel.tscn
│       ├── todo_panel.tscn
│       ├── notification_panel.tscn
│       └── chief_house_marker.tscn
├── scripts/
│   ├── main.gd
│   ├── player.gd
│   ├── ui/                    # One script per UI scene
│   └── autoload/              # Global singletons (see below)
├── assets/
│   ├── sprites/               # Drop character/building PNGs here
│   ├── tilesets/              # Tiled / Godot TileMap sources
│   └── fonts/                 # Pixel fonts (e.g. DungGeunMo, PressStart2P)
└── sounds/
    ├── bgm/                   # Looping background music
    └── sfx/                   # UI clicks, timer dings
```

### Autoloaded singletons

These are always available from any script by name.

| Name | Responsibility |
|---|---|
| `GameState` | Chief name, total focus cycles, day index, unlocks |
| `TimeManager` | Pomodoro state machine (Focus → Break → Idle) |
| `TodoManager` | Add / toggle / remove / clear today's tasks |
| `NotificationBus` | Emit + history of in-game toasts |
| `SaveManager` | JSON autosave every 30 s + on window close |

Save file lives at `user://save.json` — on Linux that resolves to
`~/.local/share/godot/app_userdata/몽글마을 (Mongle Village)/save.json`.

---

## 🎨 Replacing the placeholder art

The current player sprite is a magenta `PlaceholderTexture2D` and the village
background is a flat green `ColorRect`. To make it look like the mockup:

1. Buy/grab a Stardew-style tileset from
   [itch.io](https://itch.io/game-assets/free/tag-pixel-art) or
   [Kenney.nl](https://kenney.nl/assets) (recommended: *Cozy Farm*,
   *Sprout Lands*, *Stardew Valley Concerned Ape Pixel Font*).
2. Drop the PNGs into `assets/sprites/` and `assets/tilesets/`.
3. In `scenes/main.tscn`, replace the `Background` ColorRect with a `TileMap`
   node and paint your village.
4. In `scenes/player.tscn`, swap the `Sprite2D`'s texture for your character
   PNG (and consider promoting it to an `AnimatedSprite2D` with idle/walk
   animations).

For pixel-perfect rendering the project already sets
`textures/canvas_textures/default_texture_filter = Nearest`.

---

## 🔉 Adding sound

1. Drop `.ogg` files (Godot's preferred format) into `sounds/`.
2. Add an `AudioStreamPlayer` node to `scenes/main.tscn`, assign the BGM file,
   enable autoplay + loop.
3. For SFX (e.g. timer-done ding), call from `time_manager.gd`:
   ```gdscript
   $Sfx.stream = preload("res://sounds/sfx/ding.ogg")
   $Sfx.play()
   ```

---

## 🗺 Roadmap

- [ ] Replace placeholders with real pixel-art tileset + character spritesheet
- [ ] `AnimatedSprite2D` walk cycles for the chief
- [ ] TileMap-based village with collision on buildings
- [ ] NPC residents that unlock at cycle milestones (1, 5, 10, 25…)
- [ ] Dialogue system (Dialogic plugin)
- [ ] BGM (day/night variant) + UI SFX
- [ ] Cloud save (Supabase + JWT)
- [ ] Steam release via Godot's Steamworks plugin

---

## 📦 Building & exporting

From Godot: **Project → Export** → add a preset (Windows, Linux, macOS, Web,
Android). The first time you'll need to download the matching **export
templates** when prompted. The `.gitignore` already excludes build artifacts.

---

## 🤝 Credits

- Engine: Godot 4 — MIT
- Code: this repo — see LICENSE (TBD)
- Placeholder pixel art: generated within the engine; replace before release.
