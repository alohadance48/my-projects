import random
import threading
import time


def main():
    class Main:
        def __init__(self):
            self.hi = 'hi'
            self.t = []

        def hi_1(self):
            time.sleep(0.1)
            print(self.hi)

        def test(self):
            for _ in range(10):
                self.th = threading.Thread(target=self.hi_1)
                self.t.append(self.th)
                self.th.start()

            for self.t in self.t:
                self.th.join()

    Start = Main()
    Start.test()
    pass

if __name__ == '__main__':
    main()