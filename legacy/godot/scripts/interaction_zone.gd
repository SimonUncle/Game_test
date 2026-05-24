extends Area2D
## Sits in front of a building. When the player overlaps and presses
## `interact`, fires `triggered` with the configured payload. The Main
## scene listens and shows a dialogue.

signal triggered(title: String, body: String)

@export var title: String = ""
@export var body: String = ""
@export var hint_text: String = "[SPACE]"

@onready var hint_label: Label = $HintLabel

var _player_inside := false


func _ready() -> void:
	hint_label.text = hint_text
	hint_label.visible = false
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)


func _unhandled_input(event: InputEvent) -> void:
	if _player_inside and event.is_action_pressed("interact"):
		triggered.emit(title, body)


func _on_body_entered(body_node: Node) -> void:
	if body_node.is_in_group("player"):
		_player_inside = true
		hint_label.visible = true


func _on_body_exited(body_node: Node) -> void:
	if body_node.is_in_group("player"):
		_player_inside = false
		hint_label.visible = false
