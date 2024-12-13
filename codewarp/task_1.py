class NumberFilter:
    def __init__(self, array):
        self.array = array

    def filter_even_numbers(self):
        return [num for num in self.array if num % 2 == 0]

numbers = [1, 2, 3, 4, 5]
filterer = NumberFilter(numbers)
even_numbers = filterer.filter_even_numbers()
print("Четные числа:", even_numbers)
