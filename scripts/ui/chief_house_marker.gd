extends Control
## The hovering "Chief House" tag that sits over the central building,
## carrying the chief's initials. Updates when the chief name changes.

@onready var initials_label: Label = %Initials
@onready var name_label: Label = %Name


func _ready() -> void:
	GameState.chief_name_changed.connect(_refresh)
	_refresh(GameState.chief_name)


func _refresh(chief_name: String) -> void:
	var trimmed := chief_name.strip_edges()
	if trimmed.is_empty():
		initials_label.text = "?"
	else:
		var first := trimmed.substr(0, 1).to_upper()
		var rest_idx := trimmed.find(" ")
		var second := ""
		if rest_idx >= 0 and rest_idx + 1 < trimmed.length():
			second = trimmed.substr(rest_idx + 1, 1).to_upper()
		elif trimmed.length() >= 2:
			second = trimmed.substr(1, 1).to_upper()
		initials_label.text = first + second
	name_label.text = "CHIEF HOUSE"
