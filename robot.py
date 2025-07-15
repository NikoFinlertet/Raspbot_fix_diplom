import logging
import queue
import threading
import time
 
from sdl_robot.Raspbot_Lib import Raspbot
from modules.movement import MovementController
from modules.lighting import LightController
from modules.voice_control import VoiceController
from modules.gesture_control import GestureController

logger = logging.getLogger('RobotLogger')
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('logs/robot.log')
fh.setFormatter(formatter)
logger.addHandler(fh)


class Robot:
    def __init__(self):
        # Инициализация основного контроллерa
        self.bot = Raspbot()
        self.running = True

        # Очередь команд
        self.command_queue = queue.Queue()
        self.command_lock = threading.Lock()

        # Инициализация контроллеров

        self.movement = MovementController(self.bot)
        self.lighting = LightController(self.bot)
        self.voice_control = VoiceController(self.command_queue)
        self.gesture_control = GestureController(self.command_queue)

        # Состояние робота
        self.gripper_state = False
        self.wrist_angle = 90

        # Словарь команд
        self.command_map = {
            # Движение
            "move_forward": self.movement.move_forward,
            "move_backward": self.movement.move_backward,
            "turn_left": self.movement.turn_left,
            "turn_right": self.movement.turn_right,
            "stop_robot": self.movement.stop_robot,
            "emergency_stop": self.movement.emergency_stop,

            # Освещение
            "set_red_light": self.lighting.set_red_light,
            "set_green_light": self.lighting.set_green_light,
            "set_blue_light": self.lighting.set_blue_light,
            "set_yellow_light": self.lighting.set_yellow_light,
            "turn_off_light": self.lighting.turn_off_light,
            "toggle_light": self.lighting.toggle_light,

            # Световые эффекты
            "gradient_effect": lambda: self.lighting.start_light_effect('gradient', 0.02),
            "river_effect": lambda: self.lighting.start_light_effect('river', 0.01),
            "running_light_effect": lambda: self.lighting.start_light_effect('random_running', 0.1),
            "starlight_effect": lambda: self.lighting.start_light_effect('starlight', 0.1),
            "stop_light_effects": self.lighting.stop_light_effects,
        }

    def command_handler(self):
        """Обработчик команд из очереди"""
        while self.running:
            try:
                command_type, command_data = self.command_queue.get(timeout=0.5)

                with self.command_lock:

                    if command_data in self.command_map:
                        logger.info(f"Выполняю команду: {command_data}")
                        self.command_map[command_data]()
                    else:
                        logger.warning(f"Неизвестная команда: {command_data}")

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Ошибка обработки команды: {e}")

    def _check_devices(self):
        """Проверка доступности устройств"""
        devices_ok = True

        # Проверка голосового управления

        if not self.voice_control.start():
            logger.error("Не удалось инициализировать голосовое управление")
            devices_ok = False

        # Проверка управления жестами
        if not self.gesture_control.start():
            logger.error("Не удалось инициализировать управление жестами")
            devices_ok = False

        return devices_ok

    def start(self):
        """Запуск робота"""
        self._check_devices()


        Запуск потоков
        audio_thread = threading.Thread(target=self.voice_control.record_audio, daemon=True)
        audio_thread.start()

        gesture_thread = threading.Thread(target=self.gesture_control.capture_gestures, daemon=True)
        gesture_thread.start()

        command_thread = threading.Thread(target=self.command_handler, daemon=True)
        command_thread.start()

        try:
            logger.info("Робот запущен")

            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            self._shutdown()

        return True

    def _shutdown(self):
        logger.info("Выключение системы робота...")

        self.running = False

        # Аварийная остановка
        self.movement.emergency_stop()

        # Остановка контроллеров
        # self.voice_control.stop()
        self.gesture_control.stop()

        logger.info("Робот остановлен")

    # WTF?!
    def stop(self):
        """Публичный метод остановки робота"""
        self._shutdown()
