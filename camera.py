import cv2
import logging


class TapoCamera:
    def __init__(self, ip, password):
        self.rtsp_url = f"rtsp://admincam:{password}@{ip}:554/stream1"
        self.cap = None
        self.running = True

    def start(self):
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
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
