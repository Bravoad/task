"""
6.3. Создание системы автоматизации пользования пылесосом на автомойке самообслуживания.

"""
import RPi.GPIO as GPIO
import time

# Настройки GPIO пинов
PIR_PIN = 7  # Пин для PIR датчика движения
VACUUM_PIN = 8  # Пин для реле, управляющего пылесосом


def setup() -> None:
    """Настройка GPIO пинов."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.setup(VACUUM_PIN, GPIO.OUT)
    GPIO.output(VACUUM_PIN, GPIO.LOW)


def activate_vacuum(channel: int) -> None:
    """Функция активации пылесоса при обнаружении движения."""
    print("Движение обнаружено! Включение пылесоса...")
    GPIO.output(VACUUM_PIN, GPIO.HIGH)
    time.sleep(30)  # Включение пылесоса на 30 секунд
    GPIO.output(VACUUM_PIN, GPIO.LOW)
    print("Пылесос выключен.")


def main() -> None:
    """Основная функция для настройки и запуска системы."""
    setup()

    # Привязка функции к событию обнаружения движения
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=activate_vacuum)

    try:
        while True:
            time.sleep(1)  # Основной цикл для поддержания работы скрипта
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Система остановлена и очищена.")


# Запуск основной функции
if __name__ == "__main__":
    main()
