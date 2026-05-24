extends Node2D
## Main village scene. Wires HUD signals, top-nav popups, and forwards
## interaction-zone triggers to the bottom dialogue box.

@onready var top_nav: PanelContainer = $UILayer/TopNav
@onready var date_panel: PanelContainer = $UILayer/DatePanel
@onready var todo_panel: PanelContainer = $UILayer/TodoPanel
@onready var popup: AcceptDialog = $UILayer/InfoDialog
@onready var dialogue_box = $UILayer/DialogueBox


func _ready() -> void:
	top_nav.nav_pressed.connect(_on_nav_pressed)
	date_panel.add_pressed.connect(todo_panel.focus_input)

	for zone in get_tree().get_nodes_in_group("interaction_zone"):
		zone.triggered.connect(_on_zone_triggered)


func _on_nav_pressed(target: String) -> void:
	match target:
		"town_info":
			_show_dialog("마을 정보",
				"몽글마을 — 총 %d번의 집중 사이클이 쌓였어요." % GameState.total_focus_cycles)
		"residents":
			var count := GameState.unlocked_residents.size()
			_show_dialog("주민들",
				"현재 주민: %d명. 사이클을 완료할수록 한 명씩 이사 옵니다." % count)
		"settings":
			_show_dialog("설정", "환경설정 화면은 곧 추가됩니다.")
		"login":
			_show_dialog("로그인", "현재 게스트로 플레이 중입니다.")


func _on_zone_triggered(title: String, body: String) -> void:
	dialogue_box.show_dialogue(title, body)


func _show_dialog(title: String, body: String) -> void:
	popup.title = title
	popup.dialog_text = body
	popup.popup_centered()
