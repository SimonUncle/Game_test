extends PanelContainer
## Top-right date card. Shows YYYY.MM.DD and weekday, plus a + button
## that hands focus to the todo input field below.

signal add_pressed

@onready var date_label: Label = %DateLabel
@onready var weekday_label: Label = %WeekdayLabel
@onready var add_button: Button = %AddButton

const WEEKDAYS_EN := ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]


func _ready() -> void:
	add_button.pressed.connect(func(): add_pressed.emit())
	_refresh()
	# Refresh once a minute — enough for the date to flip at midnight
	var t := Timer.new()
	t.wait_time = 60.0
	t.autostart = true
	t.timeout.connect(_refresh)
	add_child(t)


func _refresh() -> void:
	var d := Time.get_datetime_dict_from_system()
	date_label.text = "%04d.%02d.%02d" % [d.year, d.month, d.day]
	weekday_label.text = WEEKDAYS_EN[d.weekday]
