

class Menu :
    def __init__(self,balance:int,level:int):
        self.balance = balance
        self.level = level

    def func(self):
        print(f'Ваш баланс : {self.balance}',f'Ваш уровень : {self.level }')
        print(f'Следующий  уровень : {self.level + 1 }')
        print(f'Доступные места : магазин , следующий уровень')
        choice = input('Куда отправимся ?')
        if choice == 'магазин':
            pass
        elif choice == 'уровень следующий уровень ' :
            pass




