extends CharacterBody2D
## Wandering chicken NPC. Picks a random nearby waypoint every few seconds
## and toddles toward it; idles in between.

@export var speed: float = 22.0
@export var wander_radius: float = 90.0
@export var idle_min: float = 1.0
@export var idle_max: float = 3.0

const FRAME_W := 16
const FRAME_H := 16
const ANIM_FPS := 4.0

@onready var sprite: Sprite2D = $Sprite2D

var _home: Vector2
var _target: Vector2
var _state := "idle"          # "idle" or "walk"
var _state_timer: Timer
var _frame_col := 0
var _frame_accum := 0.0
var _atlas: AtlasTexture


func _ready() -> void:
	_home = global_position
	_target = _home

	var sheet := load("res://assets/sprites/chicken_sheet.png") as Texture2D
	_atlas = AtlasTexture.new()
	_atlas.atlas = sheet
	_atlas.region = Rect2(0, 0, FRAME_W, FRAME_H)
	sprite.texture = _atlas

	_state_timer = Timer.new()
	_state_timer.one_shot = true
	_state_timer.timeout.connect(_pick_next)
	add_child(_state_timer)
	_state_timer.start(randf_range(idle_min, idle_max))


func _physics_process(delta: float) -> void:
	if _state == "walk":
		var to_target := _target - global_position
		if to_target.length() < 4.0:
			_enter_idle()
		else:
			velocity = to_target.normalized() * speed
			move_and_slide()
			sprite.flip_h = velocity.x < 0
			_frame_accum += delta * ANIM_FPS
			if _frame_accum >= 1.0:
				_frame_accum = 0.0
				_frame_col = 1 - _frame_col
	else:
		velocity = Vector2.ZERO

	_atlas.region = Rect2(_frame_col * FRAME_W, 0, FRAME_W, FRAME_H)


func _pick_next() -> void:
	if _state == "idle":
		var angle := randf() * TAU
		var dist := randf_range(20.0, wander_radius)
		_target = _home + Vector2(cos(angle), sin(angle)) * dist
		_state = "walk"
		# Safety: bail back to idle if we don't arrive within ~6 seconds
		_state_timer.start(6.0)
	else:
		_enter_idle()


func _enter_idle() -> void:
	_state = "idle"
	velocity = Vector2.ZERO
	_state_timer.start(randf_range(idle_min, idle_max))
