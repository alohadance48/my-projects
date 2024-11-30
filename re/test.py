class Test:
    def __init__(self, list_user):
        self.list_int = set()  # Используем множество для целых чисел
        self.list_int_minus = set()  # Используем множество для отрицательных или нецелых чисел
        self.list_str = set()  # Используем множество для строк
        self.list_bool = set()  # Используем множество для булевых значений
        self.list_user = list_user

    def process(self):
        for item in self.list_user:
            if isinstance(item, str):
                self.list_str.add(item)
            elif isinstance(item, int):
                self.list_int.add(item)
            elif isinstance(item, bool):
                self.list_bool.add(item)
            else:
                self.list_int_minus.add(item)

        # Преобразуем множества обратно в списки
        return list(self.list_bool), list(self.list_int), list(self.list_int_minus), list(self.list_str)


# Пример использования
list_data = [1, 2, 3, 4, '1', True, False, '1', -5, 2, True]  # Включены дубликаты
start = Test(list_data)
bools, integers, integers_minus, strings = start.process()

# Упорядоченный и понятный вывод
print("Результаты обработки списка:")
print(f"Булевые значения: {list(bools)}")  # Преобразуем в список для отображения
print(f"Целые числа: {list(integers)}")  # Преобразуем в список для отображения
print(f"Отрицательные или нецелые числа: {list(integers_minus)}")  # Преобразуем в список для отображения
print(f"Строки: {list(strings)}")  # Преобразуем в список для отображения