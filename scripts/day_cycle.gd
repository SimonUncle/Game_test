extends CanvasModulate
## Smoothly cycles the world's color modulation through morning / noon /
## evening / night over CYCLE_DURATION seconds of real time. The UI layer
## sits on a separate CanvasLayer above this, so HUD stays unaffected.

@export var cycle_duration: float = 90.0

const PHASES := [
	{"name": "DAWN",    "color": Color(1.00, 0.90, 0.78, 1.0)},
	{"name": "NOON",    "color": Color(1.00, 1.00, 1.00, 1.0)},
	{"name": "DUSK",    "color": Color(1.00, 0.72, 0.50, 1.0)},
	{"name": "NIGHT",   "color": Color(0.42, 0.48, 0.78, 1.0)},
]

var _elapsed: float = 0.0


func _process(delta: float) -> void:
	_elapsed += delta
	var t: float = fmod(_elapsed, cycle_duration) / cycle_duration
	var pos: float = t * PHASES.size()
	var a: int = int(pos) % PHASES.size()
	var b: int = (a + 1) % PHASES.size()
	var frac: float = pos - floor(pos)
	# smoothstep for nicer transitions
	frac = smoothstep(0.0, 1.0, frac)
	color = PHASES[a].color.lerp(PHASES[b].color, frac)
