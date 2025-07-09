import logging
import threading
from sdl_robot.Raspbot_Lib import Raspbot


class MovementController:
    def __init__(self, bot):
        self.bot = bot

        # Настройки движения
        self.MOVE_DURATION = 0.35
        self.TURN_DURATION = 0.15
        self.MAIN_SPEED = 150
        self.TURN_OFF_SPEED = 100

        # Таймер для автоматической остановки
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
        logging.info("АВАРИЙНАЯ ОСТАНОВКА")

    def move_forward(self):
        """Движение вперед"""
        self._cancel_timer()
        for motor_id in range(4):
            self._set_motor(motor_id, 0, self.MAIN_SPEED)
        self.action_timer = threading.Timer(self.MOVE_DURATION, self._emergency_stop)
        self.action_timer.start()
        logging.info("Движение вперед")

    def move_backward(self):
        """Движение назад"""
        self._cancel_timer()
        for motor_id in range(4):
            self._set_motor(motor_id, 1, self.MAIN_SPEED)
        self.action_timer = threading.Timer(self.MOVE_DURATION, self._emergency_stop)
        self.action_timer.start()
        logging.info("Движение назад")

    def turn_left(self):
        """Поворот налево"""
        self._cancel_timer()
        for m in [0, 1]:
            self._set_motor(m, 1, self.TURN_OFF_SPEED)
        for m in [2, 3]:
            self._set_motor(m, 0, self.MAIN_SPEED)
        self.action_timer = threading.Timer(self.TURN_DURATION, self._emergency_stop)
        self.action_timer.start()
        logging.info("Поворот налево")

    def turn_right(self):
        """Поворот направо"""
        self._cancel_timer()
        for m in [2, 3]:
            self._set_motor(m, 1, self.TURN_OFF_SPEED)
        for m in [0, 1]:
            self._set_motor(m, 0, self.MAIN_SPEED)
        self.action_timer = threading.Timer(self.TURN_DURATION, self._emergency_stop)
        self.action_timer.start()
        logging.info("Поворот направо")

    def stop_robot(self):
        """Полная остановка робота"""
        self._emergency_stop()
        logging.info("ПОЛНАЯ ОСТАНОВКА")
