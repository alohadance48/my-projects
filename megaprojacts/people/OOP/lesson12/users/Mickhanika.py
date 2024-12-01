
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

