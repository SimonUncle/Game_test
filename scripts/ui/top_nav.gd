extends PanelContainer
## Top navigation strip — TOWN INFO / RESIDENTS / SETTINGS on the left,
## the village name centered, GUEST + LOGIN on the right.
##
## All buttons emit a typed signal so the Main scene decides what to open.

signal nav_pressed(target: String)

@onready var town_info_btn: Button = %TownInfo
@onready var residents_btn: Button = %Residents
@onready var settings_btn: Button = %Settings
@onready var login_btn: Button = %Login
@onready var title_label: Label = %Title
@onready var guest_label: Label = %Guest


func _ready() -> void:
	town_info_btn.pressed.connect(func(): nav_pressed.emit("town_info"))
	residents_btn.pressed.connect(func(): nav_pressed.emit("residents"))
	settings_btn.pressed.connect(func(): nav_pressed.emit("settings"))
	login_btn.pressed.connect(func(): nav_pressed.emit("login"))
	title_label.text = "몽글마을"
	guest_label.text = "GUEST"
