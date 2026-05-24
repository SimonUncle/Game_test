extends PanelContainer
## Bottom-right toast/notification panel. Shows the most recent notification
## from NotificationBus. Auto-fades after a few seconds; can be dismissed
## manually with the × button.

@onready var title_label: Label = %Title
@onready var body_label: Label = %Body
@onready var sender_label: Label = %Sender
@onready var time_label: Label = %TimeAgo
@onready var close_button: Button = %Close
@onready var hide_timer: Timer = $HideTimer


func _ready() -> void:
	NotificationBus.pushed.connect(_on_pushed)
	close_button.pressed.connect(hide)
	hide_timer.timeout.connect(hide)

	# Seed with welcome ping
	NotificationBus.push(
		"welcome",
		"오늘도 힘내세요!",
		"하나씩 해나가면 돼요. 몽글마을이 응원합니다."
	)


func _on_pushed(notif: Dictionary) -> void:
	title_label.text = notif.title
	body_label.text = notif.body
	sender_label.text = "몽글마을 주민회"
	time_label.text = "방금 전"
	show()
	modulate = Color(1, 1, 1, 0)
	var tw := create_tween()
	tw.tween_property(self, "modulate:a", 1.0, 0.25)
	hide_timer.start()
