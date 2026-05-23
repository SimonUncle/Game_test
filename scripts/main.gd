extends Node2D
## Main village scene. Wires up the HUD signals and routes top-nav clicks
## to placeholder popups (Town Info / Residents / Settings / Login).

@onready var top_nav: PanelContainer = $UILayer/TopNav
@onready var date_panel: PanelContainer = $UILayer/DatePanel
@onready var todo_panel: PanelContainer = $UILayer/TodoPanel
@onready var popup: AcceptDialog = $UILayer/InfoDialog


func _ready() -> void:
	top_nav.nav_pressed.connect(_on_nav_pressed)
	date_panel.add_pressed.connect(todo_panel.focus_input)


func _on_nav_pressed(target: String) -> void:
	match target:
		"town_info":
			_show_dialog("마을 정보",
				"몽글마을 — 오늘 %d번째 사이클을 함께하는 중입니다." % GameState.total_focus_cycles)
		"residents":
			_show_dialog("주민들",
				"아직 만난 주민이 없어요. 첫 사이클을 끝내면 한 명이 이사옵니다.")
		"settings":
			_show_dialog("설정", "환경설정은 곧 추가될 예정이에요.")
		"login":
			_show_dialog("로그인", "현재 게스트로 플레이 중입니다.")


func _show_dialog(title: String, body: String) -> void:
	popup.title = title
	popup.dialog_text = body
	popup.popup_centered()
