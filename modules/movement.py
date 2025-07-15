from config import MOVE_DURATION, TURN_DURATION, MAIN_SPEED, TURN_OFF_SPEED
import logging
import threading
from sdl_robot.Raspbot_Lib import Raspbot

logger = logging.getLogger('movementLogger')
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('logs/module_movement.log')
fh.setFormatter(formatter)
logger.addHandler(fh)


class MovementController:
    def __init__(self, bot):
        self.bot = bot

        # Тaймер для автоматической остановки
        self.action_timer = None

    def _set_motor(self, motor_id, direction, speed):
        """Установить параметры мотора"""
        self.bot.Ctrl_Car(motor_id, direction, speed)

    def _emergency_stop(self):
        """Немедленная остановка всех моторов"""
        for motor_id in range(4):
            self._set_motor(motor_id, 0, 0)

    def _cancel_timer(self):
        """Отменить таймер автоматической остановки"""
        if self.action_timer:
            self.action_timer.cancel()
            self.action_timer = None

    def emergency_stop(self):
        """Аварийная остановка с сбросом сервоприводов и света"""
        self._emergency_stop()
        self.bot.Ctrl_Servo(2, 0)
        self.bot.Ctrl_Servo(1, 90)
        self.bot.Ctrl_WQ2812_ALL(0, 0)
        logger.info("АВАРИЙНАЯ ОСТАНОВКА")

    def move_forward(self):
        """Движение вперед"""
        self._cancel_timer()
        for motor_id in range(4):
            self._set_motor(motor_id, 0, MAIN_SPEED)
        self.action_timer = threading.Timer(MOVE_DURATION, self._emergency_stop)
        self.action_timer.start()
        logger.info("Движение вперед")

    def move_backward(self):
        """Движение назад"""
        self._cancel_timer()
        for motor_id in range(4):
            self._set_motor(motor_id, 1, MAIN_SPEED)
        self.action_timer = threading.Timer(MOVE_DURATION, self._emergency_stop)
        self.action_timer.start()
        logger.info("Движение назад")

    def turn_left(self):
        """Поворот налево"""
        self._cancel_timer()
        for m in [0, 1]:
            self._set_motor(m, 1, TURN_OFF_SPEED)
        for m in [2, 3]:
            self._set_motor(m, 0, MAIN_SPEED)
        self.action_timer = threading.Timer(TURN_DURATION, self._emergency_stop)
        self.action_timer.start()
        logger.info("Поворот налево")

    def turn_right(self):
        """Поворот направо"""
        self._cancel_timer()
        for m in [2, 3]:
            self._set_motor(m, 1, TURN_OFF_SPEED)
        for m in [0, 1]:
            self._set_motor(m, 0, MAIN_SPEED)
        self.action_timer = threading.Timer(TURN_DURATION, self._emergency_stop)
        self.action_timer.start()
        logger.info("Поворот направо")

    def stop_robot(self):
        """Полная остановка робота"""
        self._emergency_stop()
        logger.info("ПОЛНАЯ ОСТАНОВКА")
