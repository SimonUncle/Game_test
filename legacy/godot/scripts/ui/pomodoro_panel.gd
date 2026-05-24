extends PanelContainer
## Big focus-time HUD in the top-left. Mirrors the screenshot:
## an icon chip, "25:00" big numerals, "<< FOCUS TIME >>" subtitle,
## cycle counter, START / RESET row.

@onready var time_label: Label = %TimeLabel
@onready var phase_label: Label = %PhaseLabel
@onready var cycles_label: Label = %CyclesLabel
@onready var start_button: Button = %StartButton
@onready var reset_button: Button = %ResetButton


func _ready() -> void:
	TimeManager.tick.connect(_on_tick)
	TimeManager.state_changed.connect(_on_state_changed)
	GameState.cycle_completed.connect(_on_cycle_completed)

	start_button.pressed.connect(_on_start_pressed)
	reset_button.pressed.connect(_on_reset_pressed)

	_refresh_all()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("toggle_timer"):
		_on_start_pressed()


func _on_start_pressed() -> void:
	match TimeManager.state:
		TimeManager.State.IDLE:
			TimeManager.start_focus()
		_:
			if TimeManager.is_running():
				TimeManager.pause()
			else:
				TimeManager.resume()
	_refresh_button_labels()


func _on_reset_pressed() -> void:
	TimeManager.reset()
	_refresh_button_labels()


func _on_tick(secs: int) -> void:
	time_label.text = TimeManager.format_mmss(secs)


func _on_state_changed(_s: int) -> void:
	_refresh_all()


func _on_cycle_completed(total: int) -> void:
	cycles_label.text = "%d CYCLES" % total


func _refresh_all() -> void:
	time_label.text = TimeManager.format_mmss(TimeManager.seconds_left)
	cycles_label.text = "%d CYCLES" % GameState.total_focus_cycles
	phase_label.text = _phase_text()
	_refresh_button_labels()


func _refresh_button_labels() -> void:
	match TimeManager.state:
		TimeManager.State.IDLE:
			start_button.text = "▶ START"
		_:
			start_button.text = "❚❚ PAUSE" if TimeManager.is_running() else "▶ RESUME"


func _phase_text() -> String:
	match TimeManager.state:
		TimeManager.State.FOCUS:
			return "<<  FOCUS TIME  >>"
		TimeManager.State.BREAK_SHORT:
			return "<<  SHORT BREAK  >>"
		TimeManager.State.BREAK_LONG:
			return "<<  LONG BREAK  >>"
		_:
			return "<<  FOCUS TIME  >>"
