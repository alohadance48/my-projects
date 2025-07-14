import random

class Main:
    def __init__(self, massive):
        self.massive = massive
        self.int_massive = []
        self.int_minus_massive = []
        self.massive_string = []
        self.bool_massive = []
        self.float_massive = []

    def sort(self):
        for element in self.massive:
            match element:
                case bool():
                    self.bool_massive.append(element)
                    self.bool_massive.sort()
                case int():
                    if element < 0:
                        self.int_minus_massive.append(element)
                        self.int_minus_massive.sort()
                    else:
                        self.int_massive.append(element)
                        self.int_massive.sort()
                case str():
                    self.massive_string.append(element)
                case float():
                    self.float_massive.append(element)
                case _:
                    print(f"Неизвестный тип: {element}")

# Генерация случайного массива
massive = [random.choice([True, False, random.randint(-1000000000, 1000000), "Hello", 3.14]) for _ in range(100)]

main_instance = Main(massive)
main_instance.sort()

print("Булевы значения:", main_instance.bool_massive)
print("Целые числа:", main_instance.int_massive)
print("Отрицательные целые числа:", main_instance.int_minus_massive)
print("Строки:", main_instance.massive_string)
print('Не целые число',main_instance.float_massive)