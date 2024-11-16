import time
import random


def heart_failure(fatigue:int,old:int,start:bool):
    if fatigue == 100 and old >= 55 and start == True :
        print('У вас огромная нагрузка на сердце , если в течение 10 секунд не сбросить нагрузку вы умрете с шансом 70 %')
        time.sleep(10)
        chance = random.randint(1,10)
        if chance <= 7 :
            print('Вы погибли')
            dead = True
            pass
        else :
            print('Вы выжили !')
            dead = False
            pass



heart_failure(100,55,True)