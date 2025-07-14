import RPi.GPIO as GPIO
from datetime import datetime
import time


class OffPin:
    def __init__(self):
        self.pins_numbers = [4, 6]
        GPIO.setmode(GPIO.BCM)  # Установка режима BCM один раз

    def off_pins(self):
        try:
            for pin in self.pins_numbers:
                GPIO.setup(pin, GPIO.OUT)
                print(f"Отключение пина {pin}...")
                GPIO.output(pin, False)

        except KeyboardInterrupt:
            print("\nВыход из программы...")

    def cleanup(self):
        """Безопасное отключение всех пинов"""
        print("Очищаю все пины...")
        GPIO.cleanup()


class TimeOffOn(OffPin):
    def time_off(self):
        day = datetime.today().weekday()
        work_days = {1, 2, 3, 4}  # Используем множество для быстродействия

        if day in work_days:
            now = datetime.now()
            if now.hour == 1 and now.minute == 0:
                self.off_pins()
            else:
                for pin in self.pins_numbers:
                    try:
                        GPIO.setup(pin, GPIO.OUT)
                        print(f"Включаю пин {pin}...")
                        GPIO.output(pin, True)  # Включаем пин
                    except KeyboardInterrupt:
                        print("\nВыход из программы...")


# Запуск
if __name__ == "__main__":
    controller = TimeOffOn()

    try:
        while True:
            controller.time_off()
            time.sleep(1)  # Проверяем каждую секунду
    except KeyboardInterrupt:
        controller.cleanup()
