extends Node
## Pomodoro focus timer. Autoloaded as `TimeManager`.
##
## States: IDLE → FOCUS → BREAK → IDLE
## Classic 25/5 minute cycle with a long 15-minute break every 4th cycle.
## The UI binds to the signals; nothing else should mutate state directly.

signal state_changed(new_state: int)
signal tick(seconds_left: int)
signal cycle_finished(was_focus: bool)

enum State { IDLE, FOCUS, BREAK_SHORT, BREAK_LONG }

const FOCUS_DURATION := 25 * 60
const SHORT_BREAK := 5 * 60
const LONG_BREAK := 15 * 60
const LONG_BREAK_EVERY := 4

var state: State = State.IDLE
var seconds_left: int = FOCUS_DURATION
var cycles_in_set: int = 0          # resets after a long break

var _timer: Timer


func _ready() -> void:
	_timer = Timer.new()
	_timer.wait_time = 1.0
	_timer.one_shot = false
	_timer.autostart = false
	_timer.timeout.connect(_on_second_tick)
	add_child(_timer)


func start_focus() -> void:
	state = State.FOCUS
	seconds_left = FOCUS_DURATION
	_timer.start()
	state_changed.emit(state)
	tick.emit(seconds_left)


func start_break() -> void:
	var is_long := (cycles_in_set > 0) and (cycles_in_set % LONG_BREAK_EVERY == 0)
	state = State.BREAK_LONG if is_long else State.BREAK_SHORT
	seconds_left = LONG_BREAK if is_long else SHORT_BREAK
	_timer.start()
	state_changed.emit(state)
	tick.emit(seconds_left)


func pause() -> void:
	_timer.stop()


func resume() -> void:
	if state != State.IDLE and seconds_left > 0:
		_timer.start()


func reset() -> void:
	_timer.stop()
	state = State.IDLE
	seconds_left = FOCUS_DURATION
	state_changed.emit(state)
	tick.emit(seconds_left)


func is_running() -> bool:
	return not _timer.is_stopped()


func format_mmss(secs: int) -> String:
	var m := secs / 60
	var s := secs % 60
	return "%02d:%02d" % [m, s]


func _on_second_tick() -> void:
	seconds_left -= 1
	tick.emit(seconds_left)
	if seconds_left <= 0:
		_timer.stop()
		_advance_state()


func _advance_state() -> void:
	match state:
		State.FOCUS:
			cycles_in_set += 1
			GameState.register_completed_cycle()
			cycle_finished.emit(true)
			NotificationBus.push(
				"focus_done",
				"집중 끝!",
				"한 사이클 완료! 5분 쉬어가요 🌿"
			)
			start_break()
		State.BREAK_SHORT, State.BREAK_LONG:
			cycle_finished.emit(false)
			NotificationBus.push(
				"break_done",
				"휴식 끝",
				"몽글마을이 다시 집중을 기다려요."
			)
			reset()
		_:
			reset()
