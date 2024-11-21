# deastole.py
import time
from info import Info

class DestoleMain:
    def __init__(self, deastole_start: bool):
        self.deastole_start = deastole_start
        self.blood_ejection_status = False
        self.info_instance = Info()

    def deastole(self):
        self.blood_ejection_status = True
        self.info_instance.deastole(self.blood_ejection_status)

    def sistole(self):
        self.blood_ejection_status = False
        self.info_instance.deastole(self.blood_ejection_status)

    def get_blood_status(self):
        return self.blood_ejection_status

class Deastole(DestoleMain):
    def main_start(self):
        i = 0
        while self.deastole_start:
            i  += 1
            if i  == 1:
                time.sleep(2)
                self.deastole()
            else:
                time.sleep(2)
                self.sistole()
                i = 0

