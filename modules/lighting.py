import logging
import threading
from sdl_robot.Raspbot_Lib import Raspbot, LightShow

logger = logging.getLogger('lighting_logger')
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('logs/module_lighting.log')
fh.setFormatter(formatter)
logger.addHandler(fh)


class LightController:
    def __init__(self, bot):
        self.bot = bot
        self.light_show = LightShow()

        # Состояние освeщения
        self.current_light = 0
        self.light_state = False

    def set_red_light(self):
        """Включить красный свет"""
        self.bot.Ctrl_WQ2812_ALL(1, 0)
        self.current_light = 1
        logger.info("Красный свет")

    def set_green_light(self):
        """Включить зеленый свет"""
        self.bot.Ctrl_WQ2812_ALL(1, 1)
        self.current_light = 2
        logger.info("Зеленый свет")

    def set_blue_light(self):
        """Включить синий свет"""
        self.bot.Ctrl_WQ2812_ALL(1, 2)
        self.current_light = 3
        logger.info("Синий свет")

    def set_yellow_light(self):
        """Включить желтый свет"""
        self.bot.Ctrl_WQ2812_ALL(1, 3)
        self.current_light = 4
        logger.info("Желтый свет")

    def turn_off_light(self):
        """Выключить свет"""
        self.bot.Ctrl_WQ2812_ALL(0, 0)
        self.current_light = 0
        logger.info("Свет выключен")

    def toggle_light(self):
        """Переключить состояние света"""
        if self.light_state:
            self.turn_off_light()
        else:
            self.set_blue_light()
        self.light_state = not self.light_state
        logger.info("Переключение света")

    def start_light_effect(self, effect_name, speed):
        """Запустить световой эффект"""
        self.light_show.stop()
        self.light_show.running = True
        threading.Thread(
            target=self.light_show.execute_effect,
            args=(effect_name, 9999, speed, 0),
            daemon=True
        ).start()
        logger.info(f"Запущен световой эффект: {effect_name}")

    def stop_light_effects(self):
        """Остановить все световые эффекты"""
        self.light_show.stop()
        self.light_show.turn_off_all_lights()
        logger.info("Световые эффекты выключены")
