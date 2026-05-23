extends CharacterBody2D
## Chief character. 4-directional movement with a 2-frame walk cycle
## driven by an AtlasTexture region on the spritesheet
## (rows = down/left/right/up; cols = step 0 / step 1).

@export var speed: float = 110.0

const FRAME_W := 16
const FRAME_H := 24
const ANIM_FPS := 6.0

@onready var sprite: Sprite2D = $Sprite2D

var _direction_row := 0      # 0=down 1=left 2=right 3=up
var _frame_col := 0
var _frame_accum := 0.0
var _atlas: AtlasTexture


func _ready() -> void:
	# Spritesheet is loaded by the scene; wrap it in an AtlasTexture so
	# we can swap regions every frame without preloading per-frame textures.
	var sheet := load("res://assets/sprites/chief_sheet.png") as Texture2D
	_atlas = AtlasTexture.new()
	_atlas.atlas = sheet
	_atlas.region = Rect2(0, 0, FRAME_W, FRAME_H)
	sprite.texture = _atlas
	sprite.flip_h = false


func _physics_process(delta: float) -> void:
	var input_vec := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = input_vec * speed
	move_and_slide()

	if input_vec.length() > 0.05:
		_update_direction(input_vec)
		_frame_accum += delta * ANIM_FPS
		if _frame_accum >= 1.0:
			_frame_accum = 0.0
			_frame_col = 1 - _frame_col
	else:
		_frame_col = 0
		_frame_accum = 0.0

	_atlas.region = Rect2(
		_frame_col * FRAME_W,
		_direction_row * FRAME_H,
		FRAME_W, FRAME_H
	)


func _update_direction(v: Vector2) -> void:
	if abs(v.x) > abs(v.y):
		_direction_row = 1 if v.x < 0 else 2
	else:
		_direction_row = 3 if v.y < 0 else 0
