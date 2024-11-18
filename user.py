from old import User
from info import Info

def main():
    class DescriptionOfTheHeart:
        def __init__(self):
            self.user_old = int(input('Сколько лет организму: '))

        def paraments(self):
            user_age = self.user_old
            start = User(user_age)
            chance = start.chance_main()  # Получаем шанс недуга
            main_info = Info()
            main_info.user_info(user_age)
            print(f'Симуляция началась, ваши параметры: года {user_age}, шанс недуга: {chance}')

    test = DescriptionOfTheHeart()
    test.paraments()

if __name__ == '__main__':
    main()
