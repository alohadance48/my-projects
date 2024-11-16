import random

class User:
    def __init__(self, age: int):
        self.age = age
        self.chance = False

    def chance_main(self): # метод для расчета шанса недуга
        if self.age >= 55:
            chance_value = random.randint(1, 2) #расчет шанса
            if chance_value == 1:
                self.chance = True
            else:
                self.chance = False
        else:
            self.chance = False
        return self.chance
    '''Если возраст который задает user 55 лет или больше - недуг с шансом 50 процентов .
      Если есть недуг - переменная (chance) содержит True , если нету недуга - False.
      Все эти данный для передачи в основной модуль .'''


test = User(55)
print(test.chance_main())


