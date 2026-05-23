extends Node
## In-game notification bus. Autoloaded as `NotificationBus`.
##
## Any system pushes a notification; the Notification UI panel subscribes
## and displays it. Keeps a short history so the panel can show recent items.

signal pushed(notif: Dictionary)

const HISTORY_LIMIT := 20

var history: Array = []


func push(kind: String, title: String, body: String, icon_path: String = "") -> void:
	var notif := {
		"kind": kind,
		"title": title,
		"body": body,
		"icon_path": icon_path,
		"unix": Time.get_unix_time_from_system(),
	}
	history.push_front(notif)
	if history.size() > HISTORY_LIMIT:
		history.resize(HISTORY_LIMIT)
	pushed.emit(notif)
