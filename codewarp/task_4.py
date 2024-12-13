import statistics

class StatisticsCalculator:
    def __init__(self, numbers):
        self.numbers = numbers

    def calculate_statistics(self):
        mean = statistics.mean(self.numbers)
        median = statistics.median(self.numbers)
        stdev = statistics.stdev(self.numbers)
        return mean, median, stdev

numbers = [10, 20, 30, 40, 50]
stats_calculator = StatisticsCalculator(numbers)
mean, median, stdev = stats_calculator.calculate_statistics()
print(f"Среднее: {mean}, Медиана: {median}, Стандартное отклонение: {stdev}")
