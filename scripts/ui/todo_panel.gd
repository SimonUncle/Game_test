extends PanelContainer
## Todo card below the date panel. Lists today's items with a checkbox
## per row, shows the "오늘의 할 일을 추가해보세요" hint when empty, and
## accepts new items from a LineEdit (focused by the date card's + button).

@onready var list_box: VBoxContainer = %ListBox
@onready var input: LineEdit = %Input
@onready var hint: Label = %Hint


func _ready() -> void:
	TodoManager.list_changed.connect(_rebuild)
	input.text_submitted.connect(_on_submit)
	_rebuild()


func focus_input() -> void:
	input.grab_focus()


func _on_submit(text: String) -> void:
	TodoManager.add(text)
	input.clear()


func _rebuild() -> void:
	for child in list_box.get_children():
		child.queue_free()

	if TodoManager.items.is_empty():
		hint.visible = true
		return
	hint.visible = false

	for it in TodoManager.items:
		list_box.add_child(_build_row(it))


func _build_row(item: Dictionary) -> Control:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 8)

	var check := CheckBox.new()
	check.button_pressed = item.done
	check.toggled.connect(func(_p): TodoManager.toggle(item.id))
	row.add_child(check)

	var label := Label.new()
	label.text = item.text
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	label.add_theme_color_override("font_color",
		Color(0.65, 0.65, 0.65) if item.done else Color(0.95, 0.95, 0.92))
	row.add_child(label)

	var delete := Button.new()
	delete.text = "✕"
	delete.flat = true
	delete.pressed.connect(func(): TodoManager.remove(item.id))
	row.add_child(delete)

	return row
