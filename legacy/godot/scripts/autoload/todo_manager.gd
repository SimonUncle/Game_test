extends Node
## Daily todos. Autoloaded as `TodoManager`.
##
## Stored as an Array of Dictionaries: { id, text, done, created_unix }
## Persisted via SaveManager; the UI listens to `list_changed`.

signal list_changed
signal item_completed(item_id: String)

var items: Array = []


func add(text: String) -> String:
	var trimmed := text.strip_edges()
	if trimmed.is_empty():
		return ""
	var id := "%d_%d" % [Time.get_unix_time_from_system(), randi() % 10000]
	items.append({
		"id": id,
		"text": trimmed,
		"done": false,
		"created_unix": Time.get_unix_time_from_system(),
	})
	list_changed.emit()
	return id


func toggle(item_id: String) -> void:
	for it in items:
		if it.id == item_id:
			it.done = not it.done
			if it.done:
				item_completed.emit(item_id)
			list_changed.emit()
			return


func remove(item_id: String) -> void:
	for i in items.size():
		if items[i].id == item_id:
			items.remove_at(i)
			list_changed.emit()
			return


func clear_done() -> void:
	items = items.filter(func(it): return not it.done)
	list_changed.emit()


func to_dict() -> Dictionary:
	return { "items": items.duplicate(true) }


func from_dict(data: Dictionary) -> void:
	items = data.get("items", []).duplicate(true)
	list_changed.emit()
