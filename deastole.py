# destole.py
import time
from info import Info

class Destole_main:
    def __init__(self, start: bool):
        self.index = 0
        self.start_main = start
        self.blood = False
        self.info_instance = Info()

    def deastole(self):
        self.blood = True
        test = Test(self.blood)
        self.info_instance.deastole(self.blood)

    def sistole(self):
        self.blood = False
        test = Test(self.blood)
        self.info_instance.deastole(self.blood)

    def get_blood_status(self):
        return self.blood

class Deastole(Destole_main):
    def main_start(self):
        while self.start_main:
            self.index += 1
            if self.index == 1:
                time.sleep(2)
                self.deastole()
            else:
                time.sleep(2)
                self.sistole()
                self.index = 0

class Test:
    def __init__(self, status: bool):
        self.status = status
