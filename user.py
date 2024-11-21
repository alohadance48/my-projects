# user.py

import time

from old import User
from info import Info
from dead import heart_failure
from start import *
import threading


class DescriptionOfTheHeart:
    def __init__(self, user_age, fatigue, genus, root):
        self.user_old = user_age
        self.fatigue = fatigue
        self.genus = genus
        self.root = root

    def paraments(self):
        start = User(self.user_old)
        chance = start.chance_main()
        main_info = Info()
        user_info_message = main_info.user_info(self.user_old, self.fatigue)
        self.root.update_info(
            f'Симуляция началась, ваши параметры: года {self.user_old}, шанс недуга: {chance}. {user_info_message}')

        if self.user_old >= 55 and self.fatigue >= 70:
            self.heart_failure()
        else:
            run_process(True, self.root)

    def heart_failure(self):

        pass


    def timer_callback(self):
        self.root.update_info('Вы погибли из-за перегрузки на сердце.')
        info = Info()
        info.dead(True)

    def presure_drop(self):

        self.root.update_info('Вы сбросили нагрузку!')
        info = Info()
        info.dead(False)


