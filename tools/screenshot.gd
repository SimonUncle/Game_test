extends Node
## Headless screenshot helper. Attach to a node in Main during capture runs.
## Waits a few seconds (so chickens move, notif fades in), grabs the viewport,
## writes a PNG, then quits.

@export var wait_seconds: float = 2.5
@export var out_path: String = "user://screenshot.png"


func _ready() -> void:
	await get_tree().create_timer(wait_seconds).timeout
	var img := get_viewport().get_texture().get_image()
	img.save_png(out_path)
	print("Screenshot saved -> ", ProjectSettings.globalize_path(out_path))
	get_tree().quit()
