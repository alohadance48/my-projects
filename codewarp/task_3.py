class DuplicateFinder:
    def __init__(self, array):
        self.array = array

    def find_duplicates(self):
        seen = set()
        duplicates = set()
        for item in self.array:
            if item in seen:
                duplicates.add(item)
            else:
                seen.add(item)
        return duplicates

numbers = [1, 2, 3, 4, 2, 3]
finder = DuplicateFinder(numbers)
duplicates = finder.find_duplicates()
print("Дубликаты:", duplicates)
