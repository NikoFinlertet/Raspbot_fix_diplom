from config import RTSP_URL
import cv2
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/module_camera.log')
    ]
)
#Подключение
class TapoCamera:
    def __init__(self, ip, password):

        self.cap = None
        self.running = True

    def start(self):
        try:
            self.cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
            if not self.cap.isOpened():
                raise ConnectionError("Не удалось подключиться к камере")

            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_FPS, 10)
            logging.info("Камера Tapo подключена")
            return True
        except Exception as e:
            logging.error(f"Ошибка подключения к камере: {str(e)}")
            return False

    def read_frame(self):
        try:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    return frame
        except Exception as e:
            logging.error(f"Ошибка чтения кадра: {str(e)}")
        return None

    def stop(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        logging.info("Камера Tapo отключена")
