import time
import threading
from info import Info

def timer_callback():
    print('Вы умерли из-за перегрузки на сердце.')
    Info().dead(True)

def heart_failure(fatigue: int, old: int, start: bool):
    if fatigue >= 70 and old >= 55 and start:
        print('У вас огромная нагрузка на сердце. Если в течение 10 секунд не сбросить нагрузку, вы умрете с шансом 70 %.')

        timer = threading.Timer(10.0, timer_callback)
        timer.start()

        for _ in range(10):
            time.sleep(1)
            if input('Для сброса нагрузки напиши "stop": ').lower() == 'stop':
                timer.cancel()
                print('Вы сбросили нагрузку!')
                Info().dead(False)
                return
