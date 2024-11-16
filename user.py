from old import User


def main():
    class description_of_the_heart:
        def __init__(self):
            self.user_old = int(input('Сколько лет организму:'))
            pass

        def paraments(self):
            user_age = self.user_old
            start = User(user_age)
            print( f'Симуляция началась,ваши параметры :года {user_age} ')

    test = description_of_the_heart()
    test.paraments()

    pass


if __name__ == '__main__':
    main()
