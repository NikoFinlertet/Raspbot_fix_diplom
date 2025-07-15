import cv2
import logging
import time
from config import TAPO_IP, TAPO_PASSWORD
import os
from modules.hand_detector import HandDetector
from modules.camera import TapoCamera

logger = logging.getLogger('check_camera_logger')
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('logs/module_check_camera.log')
fh.setFormatter(formatter)
logger.addHandler(fh)

class CameraTester:
    def __init__(self, tapo_ip, tapo_password):
        self.tapo_camera = TapoCamera(tapo_ip, tapo_password)
        self.hand_detector = HandDetector(detectorCon=0.75)
        self.running = False
        self.test_duration = 30  # Длительность теста в секундах (0 = бесконечно)
        
    def test_camera_connection(self):
        """Проверка подключения к камере"""
        logger.info("Пытаюсь подключиться к камере...")
        if not self.tapo_camera.start():
            logger.error("Не удалось подключиться к камере!")
            return False
        
        logger.info("Камера подключена. Проверяю поток...")
        for _ in range(5):  # Проверка 5 кадров
            frame = self.tapo_camera.read_frame()
            if frame is None:
                logger.error("Не удалось получить кадр!")
                self.tapo_camera.stop()
                return False
            
            logger.info(f"Кадр получен. Размер: {frame.shape}")
            time.sleep(0.5)
        
        self.tapo_camera.stop()
        return True

    def run_hand_detection_test(self):
        """Непрерывный тест распознавания жестов"""
        logger.info(f"Запуск теста HandDetector (длительность: {self.test_duration} сек)")
        
        if not self.tapo_camera.start():
            logger.error("Ошибка подключения к камере!")
            return

        self.running = True
        start_time = time.time()
        frame_count = 0
        gesture_count = 0

        try:
            while self.running:
                # Проверка времени теста
                if self.test_duration > 0 and (time.time() - start_time) > self.test_duration:
                    logger.info("Тест завершен по времени")
                    break

                # Получение кадра
                frame = self.tapo_camera.read_frame()
                if frame is None:
                    logger.warning("Пропущен кадр")
                    continue

                frame_count += 1

                # Распознавание жестов
                frame = self.hand_detector.findHands(frame)
                gesture = self.hand_detector.get_gesture()
                
                if gesture != "None":
                    gesture_count += 1
                    logger.info(f"Обнаружен жест: {gesture}")
                    self._process_gesture(gesture)

                # Отображение информации на кадре
                fps = frame_count / (time.time() - start_time) if frame_count > 0 else 0
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Gestures: {gesture_count}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Отображение кадра
                cv2.imshow("Hand Detection Test", frame)
                
                # Выход по ESC или закрытию окна
                key = cv2.waitKey(1)
                if key == 27 or cv2.getWindowProperty("Hand Detection Test", cv2.WND_PROP_VISIBLE) < 1:
                    logger.info("Тест завершен пользователем")
                    break

        finally:
            self.running = False
            self.tapo_camera.stop()
            cv2.destroyAllWindows()
            
            # Статистика теста
            duration = time.time() - start_time
            logger.info(f"Тест завершен. Обработано кадров: {frame_count}")
            logger.info(f"Средний FPS: {frame_count/duration:.1f}")
            logger.info(f"Обнаружено жестов: {gesture_count}")

    def _process_gesture(self, gesture):
        """Обработка обнаруженного жеста (можно модифицировать)"""
        # Здесь можно добавить логику реакции на жесты
        pass

    def run_tests(self):
        """Запуск всех тестов"""
        if not self.test_camera_connection():
            return
        
        self.run_hand_detection_test()

if __name__ == "__main__":

    TEST_DURATION = 30
    tester = CameraTester(TAPO_IP, TAPO_PASSWORD)
    tester.test_duration = TEST_DURATION
    tester.run_tests()