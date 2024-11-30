class WinDoor:
    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.square = x * y

class Room:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height
        self.wd = []  # Список окон и дверей

    def add_wd(self, w, h):
        self.wd.append(WinDoor(w, h))

    def full_surface(self):
        # Полная площадь стен без учёта окон и дверей
        return 2 * self.height * (self.width + self.length)

    def work_surface(self):
        # Площадь для оклейки с учётом окон и дверей
        total_surface = self.full_surface()
        for i in self.wd:
            total_surface -= i.square
        return total_surface

    def rolls_needed(self, roll_width, roll_length):
        # Площадь одного рулона
        roll_area = roll_width * roll_length
        # Площадь для оклейки
        work_area = self.work_surface()
        # Количество рулонов, округлённое вверх
        import math
        return math.ceil(work_area / roll_area)

# Интерфейс программы
def main():
    # Запрос данных у пользователя
    width = float(input("Введите ширину комнаты (в метрах): "))
    length = float(input("Введите длину комнаты (в метрах): "))
    height = float(input("Введите высоту комнаты (в метрах): "))

    room = Room(width, length, height)

    while True:
        add_more = input("Хотите добавить окно или дверь? (да/нет): ").strip().lower()
        if add_more == 'да':
            w = float(input("Введите ширину окна/двери (в метрах): "))
            h = float(input("Введите высоту окна/двери (в метрах): "))
            room.add_wd(w, h)
        else:
            break

    print(f"Площадь оклеиваемой поверхности: {room.work_surface():.2f} кв.м")

    roll_width = float(input("Введите ширину рулона обоев (в метрах): "))
    roll_length = float(input("Введите длину рулона обоев (в метрах): "))

    rolls = room.rolls_needed(roll_width, roll_length)
    print(f"Необходимое количество рулонов: {rolls}")

if __name__ == "__main__":
    main()
