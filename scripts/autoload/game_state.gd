extends Node
## Global game state. Autoloaded as `GameState`.
##
## Tracks the village/player meta-data that persists across scenes:
## chief name, total focus cycles ever completed, current game day index,
## and a small flag bag for unlocked content.

signal day_advanced(new_day_index: int)
signal cycle_completed(total_cycles: int)
signal chief_name_changed(name: String)

const DEFAULT_CHIEF_NAME := "EJ"

var chief_name: String = DEFAULT_CHIEF_NAME:
	set(value):
		if value == chief_name:
			return
		chief_name = value
		chief_name_changed.emit(value)

var total_focus_cycles: int = 0
var game_day_index: int = 0          # days since first launch
var unlocked_residents: Array[String] = []
var unlocked_buildings: Array[String] = ["chief_house"]


func register_completed_cycle() -> void:
	total_focus_cycles += 1
	cycle_completed.emit(total_focus_cycles)


func advance_day() -> void:
	game_day_index += 1
	day_advanced.emit(game_day_index)


func to_dict() -> Dictionary:
	return {
		"chief_name": chief_name,
		"total_focus_cycles": total_focus_cycles,
		"game_day_index": game_day_index,
		"unlocked_residents": unlocked_residents,
		"unlocked_buildings": unlocked_buildings,
	}


func from_dict(data: Dictionary) -> void:
	chief_name = data.get("chief_name", DEFAULT_CHIEF_NAME)
	total_focus_cycles = int(data.get("total_focus_cycles", 0))
	game_day_index = int(data.get("game_day_index", 0))
	unlocked_residents.assign(data.get("unlocked_residents", []))
	unlocked_buildings.assign(data.get("unlocked_buildings", ["chief_house"]))
