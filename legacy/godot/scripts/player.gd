extends CharacterBody2D
## Chief character. Uses the Sparklin "Ninja Adventure" character sheet
## (CC0): 64x112, 4 cols x 7 rows of 16x16 frames.
##
##   col 0 = facing down
##   col 1 = facing up
##   col 2 = facing right  (we flip_h for left)
##   col 3 = facing right, alternate frame
##
##   row 0 = idle
##   row 4, row 5 = walk frames (alternate every step)

@export var speed: float = 110.0

const FRAME := 16
const ANIM_FPS := 6.0

const COL_DOWN := 0
const COL_UP := 1
const COL_SIDE := 2
const ROW_IDLE := 0
const ROW_WALK := [4, 5]

@onready var sprite: Sprite2D = $Sprite2D

enum Dir { DOWN, UP, LEFT, RIGHT }
var _dir: Dir = Dir.DOWN
var _walk_step := 0
var _frame_accum := 0.0
var _is_moving := false
var _atlas: AtlasTexture


func _ready() -> void:
	var sheet := load("res://assets/sparklin/character.png") as Texture2D
	_atlas = AtlasTexture.new()
	_atlas.atlas = sheet
	_atlas.region = Rect2(0, 0, FRAME, FRAME)
	sprite.texture = _atlas


func _physics_process(delta: float) -> void:
	var input_vec := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = input_vec * speed
	move_and_slide()

	_is_moving = input_vec.length() > 0.05
	if _is_moving:
		if abs(input_vec.x) > abs(input_vec.y):
			_dir = Dir.LEFT if input_vec.x < 0 else Dir.RIGHT
		else:
			_dir = Dir.UP if input_vec.y < 0 else Dir.DOWN

		_frame_accum += delta * ANIM_FPS
		if _frame_accum >= 1.0:
			_frame_accum = 0.0
			_walk_step = 1 - _walk_step
	else:
		_frame_accum = 0.0
		_walk_step = 0

	_apply_region()


func _apply_region() -> void:
	var col := _col_for_dir()
	var row: int = ROW_IDLE if not _is_moving else ROW_WALK[_walk_step]
	_atlas.region = Rect2(col * FRAME, row * FRAME, FRAME, FRAME)
	sprite.flip_h = (_dir == Dir.LEFT)


func _col_for_dir() -> int:
	match _dir:
		Dir.DOWN: return COL_DOWN
		Dir.UP:   return COL_UP
		Dir.LEFT, Dir.RIGHT: return COL_SIDE
		_: return COL_DOWN
