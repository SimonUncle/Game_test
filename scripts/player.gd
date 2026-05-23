extends CharacterBody2D
## Village wanderer. 8-directional movement, no diagonal speed boost.

@export var speed: float = 90.0

@onready var sprite: Sprite2D = $Sprite2D


func _physics_process(_delta: float) -> void:
	var input_vec := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = input_vec * speed
	move_and_slide()
	if input_vec.x != 0.0:
		sprite.flip_h = input_vec.x < 0.0
