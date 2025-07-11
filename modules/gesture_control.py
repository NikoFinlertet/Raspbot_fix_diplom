from config import TAPO_IP, TAPO_PASSWORD
import os
import logging
import time
import cv2
from modules.hand_detector import HandDetector
from modules.camera import TapoCamera


class GestureController:
    def __init__(self, command_queue):
        self.command_queue = command_queue
        self.running = True

        # Инициализация детектора жестов
        self.hand_detector = HandDetector(detectorCon=0.75)

        # Инициализация камеры
        self.tapo_camera = TapoCamera(TAPO_IP, TAPO_PASSWORD) if TAPO_IP and TAPO_PASSWORD else None
        self.local_camera = self._init_local_camera() if not self.tapo_camera else None

        # Состояние жестов
        self.last_gesture = None
        self.last_gesture_time = 0

        # Словарь команд жестов
        self.gesture_commands = {
            "One": "move_forward",
            "Two": "move_backward",
            "Three": "turn_left",
            "Four": "turn_right",
            "Fist": "emergency_stop",
        }

    def _init_local_camera(self):
        """Инициализация локальной камеры"""
        for device in ["/dev/video0", "/dev/video1"]:
            try:
                if os.path.exists(device):
                    camera = cv2.VideoCapture(device, cv2.CAP_V4L2)
                    if camera.isOpened():
                        ret, frame = camera.read()
                        if ret:
                            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
                            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
                            camera.set(cv2.CAP_PROP_FPS, 5)
                            return camera
                        camera.release()
            except Exception as e:
                logging.warning(f"Ошибка камеры {device}: {e}")
        logging.error("Локальная камера не найдена")
        return None

    def process_gesture(self, gesture):
        """Обработка распознанного жеста"""
        current_time = time.time()

        # Игнорируем повторные жесты
        if gesture == self.last_gesture and (current_time - self.last_gesture_time) < 1.0:
            return

        if gesture in self.gesture_commands:
            logging.info(f"Выполняю жест: {gesture}")
            self.command_queue.put(("gesture", self.gesture_commands[gesture]))
            self.last_gesture = gesture
            self.last_gesture_time = current_time

    def capture_gestures(self):
        """Захват и распознавание жестов"""
        if self.tapo_camera:
            if not self.tapo_camera.start():
                return
        elif not self.local_camera:
            return

        logging.info("Распознавание жестов запущено")

        while self.running:
            try:
                # Получение кадра
                if self.tapo_camera:
                    frame = self.tapo_camera.read_frame()
                else:
                    ret, frame = self.local_camera.read()
                    if not ret:
                        continue

                if frame is None:
                    time.sleep(0.1)
                    continue

                # Распознавание жестов
                frame = self.hand_detector.findHands(frame)
                gesture = self.hand_detector.get_gesture()

                if gesture != "None":
                    self.process_gesture(gesture)

                time.sleep(0.1)

            except Exception as e:
                logging.error(f"Ошибка обработки жестов: {e}")
                time.sleep(1)

    def start(self):
        """Запуск управления жестами"""
        if self.tapo_camera:
            if not self.tapo_camera.start():
                logging.error("Не удалось запустить камеру Tapo!")
                return False
            self.tapo_camera.stop()  # Остановим для повторного запуска в capture_gestures
        elif not self.local_camera:
            logging.error("Камера не найдена!")
            return False

        logging.info("Управление жестами готово к запуску")
        return True

    def stop(self):
        """Остановка управления жестами"""
        self.running = False
        if self.tapo_camera:
            self.tapo_camera.stop()
        elif self.local_camera:
            self.local_camera.release()
        logging.info("Управление жестами остановлено")
