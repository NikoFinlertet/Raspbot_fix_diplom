import os
import logging
from robot import Robot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/main.log')
    ]
)

if __name__ == "__main__":
    logging.info("Запуск Робота")

    # Освобождаем аудиоустройства
    os.system("sudo fuser -k /dev/snd/* > /dev/null 2>&1")
    os.system("sudo rmmod snd_usb_audio > /dev/null 2>&1")
    os.system("sudo modprobe snd_usb_audio > /dev/null 2>&1")

    #Робот + от камеры бело-круглой данные
    robot = Robot()

    try:
        robot.start()
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}")
