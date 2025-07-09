import cv2
import time
import logging
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, maxHands=1, detectorCon=0.5, trackCon=0.5):
        self.tipIds = [4, 8, 12, 16, 20]
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(
            static_image_mode=mode,
            max_num_hands=maxHands,
            min_detection_confidence=detectorCon,
            min_tracking_confidence=trackCon
        )
        self.lmList = []
        self.gesture = "None"
        self.last_gesture_time = 0
        self.GESTURE_COOLDOWN = 0.8  # Увеличенный кд между жестами
        self.GESTURE_HOLD_TIME = 0.5  # Жест должен держаться 0.5 сек
        self.gesture_buffer = []      # Буфер для проверки стабильности жеста
        self.buffer_size = 5          # Количество кадров для анализа

    def findHands(self, frame):
        self.lmList = []
        try:
            img_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(img_RGB)
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        self.lmList.append([id, cx, cy])
        except Exception as e:
            logging.error(f"Ошибка распознавания рук: {str(e)}")
        return frame

    def fingersUp(self):
        fingers = []
        if len(self.lmList) == 0:
            return fingers

        if len(self.lmList) > 4:
            if self.lmList[4][1] > self.lmList[3][1]:
                fingers.append(1 if self.lmList[4][1] < self.lmList[2][1] else 0)
            else:
                fingers.append(1 if self.lmList[4][1] > self.lmList[2][1] else 0)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if len(self.lmList) > self.tipIds[id] and len(self.lmList) > self.tipIds[id]-2:
                fingers.append(1 if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2] else 0)
            else:
                fingers.append(0)
        return fingers

    def get_gesture(self):
        current_time = time.time()

        # Проверка кд между жестами
        if current_time - self.last_gesture_time < self.GESTURE_COOLDOWN:
            return "None"

        # Распознаем текущий жест
        current_gesture = self._recognize_gesture()

        # Добавляем жест в буфер
        self.gesture_buffer.append(current_gesture)
        if len(self.gesture_buffer) > self.buffer_size:
            self.gesture_buffer.pop(0)

        # Проверяем, что жест стабилен в течение GESTURE_HOLD_TIME
        if (len(self.gesture_buffer) == self.buffer_size and
            all(g == current_gesture for g in self.gesture_buffer) and
            current_gesture != "None"):

            self.last_gesture_time = current_time
            self.gesture_buffer.clear()
            return current_gesture

        return "None"

    def _recognize_gesture(self):
        try:
            if len(self.lmList) == 0:
                return "None"

            fingers = self.fingersUp()
            if len(fingers) < 5:
                return "None"

            finger_count = sum(fingers)

            if finger_count == 0:
                return "Fist"
            elif finger_count == 1:
                return "One"
            elif finger_count == 2:
                return "Two"
            elif finger_count == 3:
                return "Three"
            elif finger_count == 4:
                return "Four"
            elif finger_count == 5:
                return "Five"
        except Exception as e:
            logging.error(f"Ошибка распознавания жеста: {str(e)}")
        return "Unknown"
