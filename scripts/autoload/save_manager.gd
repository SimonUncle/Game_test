extends Node
## JSON save/load. Autoloaded as `SaveManager`.
##
## File lives in `user://save.json` — that's a per-user, per-OS path
## (Godot resolves it to AppData on Windows, ~/.local/share/godot/ on Linux).

const SAVE_PATH := "user://save.json"

var _autosave_timer: Timer


func _ready() -> void:
	load_game()
	_autosave_timer = Timer.new()
	_autosave_timer.wait_time = 30.0
	_autosave_timer.autostart = true
	_autosave_timer.timeout.connect(save_game)
	add_child(_autosave_timer)
	# Save on quit too
	get_tree().auto_accept_quit = false
	get_window().close_requested.connect(_on_close_requested)


func save_game() -> void:
	var payload := {
		"version": 1,
		"saved_at_unix": Time.get_unix_time_from_system(),
		"game_state": GameState.to_dict(),
		"todos": TodoManager.to_dict(),
	}
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f == null:
		push_warning("Save failed: cannot open %s" % SAVE_PATH)
		return
	f.store_string(JSON.stringify(payload, "\t"))
	f.close()


func load_game() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if f == null:
		return
	var text := f.get_as_text()
	f.close()
	var parsed = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("Save file corrupt; ignoring.")
		return
	GameState.from_dict(parsed.get("game_state", {}))
	TodoManager.from_dict(parsed.get("todos", {}))


func _on_close_requested() -> void:
	save_game()
	get_tree().quit()
