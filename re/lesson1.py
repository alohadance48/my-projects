def pipe_fix(nums: list):
    # Находим минимальное и максимальное значение в списке
    min_num = min(nums)
    max_num = max(nums)

    # Создаем список от min_num до max_num, включая оба значения
    result = list(range(min_num, max_num +1))

    return result


# Пример использования
print(pipe_fix([1, 3, 5, 6, 7, 8]))  # Вывод: [1, 2, 3, 4, 5, 6, 7, 8]