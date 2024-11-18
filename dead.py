import time
import random
import threading
from info import Info

def timer_callback():
    pass

def heart_failure(fatigue: int, old: int, start: bool):
    if fatigue >= 70 and old >= 55 and start:
        print('У вас огромная нагрузка на сердце. Если в течение 10 секунд не сбросить нагрузку, вы умрете с шансом 70 %.')

        timer = threading.Timer(10.0, timer_callback)
        timer.start()

        for i in range(10):
            time.sleep(1)
            test = input('Для сброса нагрузки напиши stop: ')
            if test.lower() == 'stop':
                timer.cancel()
                print('Вы сбросили нагрузку!.')
                info = Info()
                info.dead(False)
                return

        chance = random.randint(1, 10)
        if chance <= 7:
            info = Info()
            info.dead(True)
        else:
            info = Info()
            info.dead(False)
