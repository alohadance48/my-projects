import time


class DestoleMain:
    def __init__(self, deastole_start: bool, defect_type: str):
        self.deastole_start = deastole_start
        self.blood_ejection_status = False
        self.defect_type = defect_type
        self.pulse = 70  # Начальный пульс

    def deastole(self):
        self.blood_ejection_status = True
        self.adjust_pulse()

    def sistole(self):
        self.blood_ejection_status = False
        self.adjust_pulse()

    def adjust_pulse(self):
        if self.defect_type == "Heart Failure":
            self.pulse = 60  # Если есть сердечная недостаточность, пульс замедляется
        elif self.defect_type == "Diabetes":
            self.pulse = 75  # Если диабет, пульс немного ускоряется
        elif self.defect_type == "Ventricular Syndrome":
            self.pulse = 80  # Синдром желудочков также ускоряет пульс
        else:
            self.pulse = 70  # Нормальный пульс без дефектов

    def get_blood_status(self):
        return "Диастола" if self.blood_ejection_status else "Систола"

    def get_pulse(self):
        return self.pulse


class Deastole(DestoleMain):
    def __init__(self, deastole_start: bool, defect_type: str):
        super().__init__(deastole_start, defect_type)
        self.time_interval = 1  # Устанавливаем значение по умолчанию для интервала

    def set_time(self, time_interval):
        self.time_interval = time_interval

    def main_start(self, update_callback, update_pulse_callback):
        while self.deastole_start:
            time.sleep(self.time_interval)
            if not self.blood_ejection_status:
                self.deastole()
                update_callback("Диастола")
            else:
                self.sistole()
                update_callback("Систола")