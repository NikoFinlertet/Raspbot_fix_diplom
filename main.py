import os
import logging
from robot import Robot

if __name__ == "__main__":
    print("Запуск Робота")

    # Освобождаем аудиоустройствa
    os.system("sudo fuser -k /dev/snd/* > /dev/null 2>&1")
    os.system("sudo rmmod snd_usb_audio > /dev/null 2>&1")
    os.system("sudo modprobe snd_usb_audio > /dev/null 2>&1")

    #Робот + от камеры бело-круглой данные
    robot = Robot()

    try:
        robot.start()
    except Exception as e:
        print.(f"Критическая ошибка: {e}")
