class Rectangle:
    def __init__(self, width, height, sign):
        self.w = int(width)
        self.h = int(height)
        self.s = str(sign)
    def __str__(self):
        rect = []
        for i in range(self.h):
            rect.append(self.s *self.w)
            rect = '\n'.join(rect)
            return rect
    def __add__(self, other):
        return Rectangle(self.w + other.w, self.h + other.h, self.s)
a = Rectangle(4, 5, 'y')
b = Rectangle(5, 5, 'z')
print(a + b)
print(b + a)