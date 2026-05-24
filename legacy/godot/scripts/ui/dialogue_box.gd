extends PanelContainer
## Bottom-screen dialogue card. Pauses player input (via process_mode) while
## visible. Closed with Space/Esc/Enter.

@onready var title_label: Label = %DialogueTitle
@onready var body_label: Label = %DialogueBody


func _ready() -> void:
	hide()


func _input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("interact") or event.is_action_pressed("ui_cancel") or event.is_action_pressed("ui_accept"):
		hide()
		get_viewport().set_input_as_handled()


func show_dialogue(title: String, body: String) -> void:
	title_label.text = title
	body_label.text = body
	show()
