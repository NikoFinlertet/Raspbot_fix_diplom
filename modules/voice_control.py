from config import SAMPLE_RATE, ALSA_DEVICE
import os
import logging
import json
import subprocess
import time
from vosk import Model, KaldiRecognizer

logger = logging.getLogger('voice_control_logger')
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('logs/module_voice_control.log')
fh.setFormatter(formatter)
logger.addHandler(fh)


class VoiceController:
    def __init__(self, command_queue):
        self.command_queue = command_queue
        self.running = True


        # Инициализация модели Vosk
        self.model = Model("model")
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)

        # Словaрь голосовых команд
        self.voice_commands = {
            "вперёд": "move_forward",
            "перед": "move_forward",
            "прямо": "move_forward",
            "стоп": "stop_robot",
            "сто": "stop_robot",
            "налево": "turn_left",
            "влево": "turn_left",
            "вправо": "turn_right",
            "направо": "turn_right",
            "назад": "move_backward",
            "красный свет": "set_red_light",
            "синий свет": "set_blue_light",
            "зеленый свет": "set_green_light",
            "зелёный свет": "set_green_light",
            "желтый свет": "set_yellow_light",
            "жёлтый свет": "set_yellow_light",
            "выключи свет": "turn_off_light",
            "выключить свет": "turn_off_light",
            "градиент": "gradient_effect",
            "течение света": "river_effect",
            "бегущий свет": "running_light_effect",
            "мерцание": "starlight_effect",
            "выключи эффекты": "stop_light_effects"
        }

    def _check_microphone(self):
        """Проверка доступности микрофона"""
        try:
            test_cmd = f"arecord -D {ALSA_DEVICE} -d 1 -f S16_LE /dev/null"
            return os.system(test_cmd) == 0
        except Exception as e:
            logger.error(f"Ошибка проверки микрофона: {e}")
            return False

    def process_voice_command(self, text):
        """Обработка голосовой команды"""
        text = text.lower()
        for command, action in self.voice_commands.items():
            if command in text:
                logger.info(f"Выполняю голосовую команду: {command}")
                self.command_queue.put(("voice", action))
                return

    def record_audio(self):
        """Непрерывная запись и распознавание речи"""
        while self.running:
            try:
                # Освобождение аудиоустройства
                os.system(f"fuser -k {ALSA_DEVICE} >/dev/null 2>&1")
                time.sleep(0.5)

                # Запуск процесса записи
                process = subprocess.Popen(
                    [
                        "arecord",
                        "-D", ALSA_DEVICE,
                        "-c", "1",
                        "-r", str(SAMPLE_RATE),
                        "-f", "S16_LE",
                        "-t", "raw"
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                logger.info(f"Запись с микрофона ({ALSA_DEVICE})")

                while self.running:
                    data = process.stdout.read(4000)
                    if not data:
                        error = process.stderr.read()
                        if error:
                            logger.error(f"Ошибка микрофона: {error.decode().strip()}")
                        time.sleep(0.1)
                        continue

                    # Распознавание речи
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get("text", "").lower()
                        if text:
                            logger.info(f"Распознано: {text}")
                            self.process_voice_command(text)

            except Exception as e:
                logger.error(f"Ошибка записи: {e}")
                time.sleep(2)
            finally:
                if 'process' in locals():
                    process.terminate()

    def start(self):
        """Запуск голосового управления"""
        if not self._check_microphone():
            logger.error("Микрофон не доступен!")
            return False

        logger.info("Голосовое управление запущено")
        return True

    def stop(self):
        """Остановка голосового управления"""
        self.running = False
        logger.info("Голосовое управление остановлено")
