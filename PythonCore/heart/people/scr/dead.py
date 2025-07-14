import threading


def timer_callback(root: object):
    root.result_label.configure(text="Вы погибли из-за перегрузки на сердце.")

def heart_failure(fatigue: int, old: int, root: object, start: bool):
    if fatigue >= 70 and old >= 55 and start:
        root.result_label.configure(text="У вас огромная нагрузка на сердце. Если в течение 10 секунд не сбросить нагрузку, вы умрете с шансом 70 %.")
        timer = threading.Timer(10.0, timer_callback, args=(root,))
        timer.start()

        return timer
    return None