def main():
    class SortMain:
        def __init__(self, massive: list):
            self.massive = massive
            self.list_int = []
            self.list_float = []
            self.list_str = []
            self.list_minus_int = []
            self.list_minus_float = []
            self.list_other = []

        def sort(self):
            for element in self.massive:
                if isinstance(element, int):
                    if element >= 0:
                        self.list_int.append(element)
                    else:
                        self.list_minus_int.append(element)
                elif isinstance(element, float):
                    if element >= 0:
                        self.list_float.append(element)
                    else:
                        self.list_minus_float.append(element)
                elif isinstance(element, str):
                    self.list_str.append(element)
                else:
                    self.list_other.append(element)

            print("Positive Integers:", self.list_int)
            print("Negative Integers:", self.list_minus_int)
            print("Positive Floats:", self.list_float)
            print("Negative Floats:", self.list_minus_float)
            print("Strings:", self.list_str)
            print("Other Types:", self.list_other)

    start = SortMain([10, 20, 30, 'str', 'int', 'float', 'min', 'max', -3.14, True, False])
    start.sort()

if __name__ == '__main__':
    main()
