import time
from info import Info

class pulse:
    pass

class DestoleMain:

    def __init__(self, start: bool):
        self.index = 0
        self.start_main = start
        self.blood = False
        self.info_instance = Info()

    def toggle_blood_status(self):
        self.blood = not self.blood
        self.info_instance.deastole(self.blood)

    def get_blood_status(self):
        return self.blood

class Deastole(DestoleMain):
    def main_start(self):
        while self.start_main:
            time.sleep(2)
            self.toggle_blood_status()
            self.index = (self.index + 1) % 2  