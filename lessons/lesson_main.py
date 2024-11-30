import math
import random

def greet_user():
    print("Добро пожаловать в калькулятор!")
    print("1. Расчет синуса и косинуса")
    print("2. Калькулятор")
    print("3. Генерация случайного числа")
    print("Для выхода введите 0.")

def calculate_sin_cos():
    try:
        angle = float(input("Введите угол в градусах: "))
        angle_radians = math.radians(angle)
        sin_value = math.sin(angle_radians)
        cos_value = math.cos(angle_radians)
        print(f"Синус {angle}°: {sin_value}")
        print(f"Косинус {angle}°: {cos_value}")
    except ValueError:
        print("Ошибка ввода. Пожалуйста, введите числовое значение.")

def basic_calculator():
    print("Выберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    choice = int(input("Ваш выбор: "))

    try:
        if choice == 1:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            print(f"Результат: {num1 + num2}")  # Исправлено
        elif choice == 2:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            print(f"Результат: {num1 - num2}")  # Исправлено
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Ошибка ввода. Пожалуйста, введите числовое значение.")

def generate_random_number():
    random_number = random.randint(1, 100)
    print(f"Ваше случайное число: {random_number}")
    if random_number > 10:
        print("Случайное число больше 10!")

def main():
    while True:
        greet_user()
        try:
            choice = int(input("Ваш выбор: "))
            if choice == 1:
                calculate_sin_cos()
            elif choice == 2:
                basic_calculator()
            elif choice == 3:
                generate_random_number()
            elif choice == 0:
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Ошибка ввода. Пожалуйста, введите числовое значение.")

if __name__ == "__main__":
    main()
