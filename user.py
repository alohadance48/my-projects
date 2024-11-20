from old import User
from info import Info
from dead import heart_failure
from start import *


class DescriptionOfTheHeart:
    def __init__(self):
        self.user_old = int(input('Сколько лет организму: '))
        self.fatigue = int(input('Твоя нагрузка (от 0 до 100): '))
        self.genus = input('Ваш пол:')

    def paraments(self):
        user_age = self.user_old
        start = User(user_age)
       # pulse(self.fatigue,self.genus,self.user_old)
        chance = start.chance_main()
        main_info = Info()
        main_info.user_info(user_age, self.fatigue)
        print(f'Симуляция началась, ваши параметры: года {user_age}, шанс недуга: {chance}')
        if self.user_old >= 55 and self.fatigue >= 70 :
            heart_failure(self.fatigue, user_age, True)
        else :
            run_process(True)





test = DescriptionOfTheHeart()
test.paraments()

