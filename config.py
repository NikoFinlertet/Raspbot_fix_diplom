# Настройки камеры
CAMERA_TYPE = "none"  # "tapo" или "local"
# TAPO_IP = "192.168.1.146"
# TAPO_PASSWORD = "qwerty"
TAPO_IP = "192.168.1.102"
TAPO_PASSWORD = "qwerty"
RTSP_URL = f"rtsp://admincam:qwerty@192.168.1.102:554/stream1"

# Настройки аудио
SAMPLE_RATE = 16000
ALSA_DEVICE = "plughw:2,0"

# Настройки движения
MOVE_DURATION = 0.35
TURN_DURATION = 0.15
MAIN_SPEED = 150
TURN_OFF_SPEED = 100

# Настройки жестов
GESTURE_COOLDOWN = 0.8
GESTURE_HOLD_TIME = 0.5
BUFFER_SIZE = 5

# Настройки света
COLOR_MAP = {
    'red': 0,
    'green': 1,
    'blue': 2,
    'yellow': 3,
    'purple': 4,
    'cyan': 5,
    'white': 6
}

LIGHT_EFFECTS = {
    'alert': ('starlight', 0.05),
    'normal': ('river', 0.1),
    'warning': ('gradient', 0.2)
}