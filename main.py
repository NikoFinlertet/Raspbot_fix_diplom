import os
import logging
from robot import Robot

logger = logging.getLogger('mainLogger')
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('logs/main.log')
fh.setFormatter(formatter)
logger.addHandler(fh)


if __name__ == "__main__":
    logger.info("Запуск Робота")

    # Освобождаем аудиоустройствa
    os.system("sudo fuser -k /dev/snd/* > /dev/null 2>&1")
    os.system("sudo rmmod snd_usb_audio > /dev/null 2>&1")
    os.system("sudo modprobe snd_usb_audio > /dev/null 2>&1")

    #Робот + от камеры бело-круглой данные
    robot = Robot()

    try:
        robot.start()
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
