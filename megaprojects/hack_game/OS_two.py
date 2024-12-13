import time
from menu import Menu
#OS_two

class HackPC:
    def __init__(self, start):
        self.start = start
        self.directory = '/home/hacker228/kali/hack/bin/command:'
        self.command = {
            'sqlinect': 'Инъекция успешно сделана!',
            'sudo connect main_backdor': (
                'Успешно получены данные:\n'
                'Admin: Rzk_Json123\n'
                'Gey_good_people: geymaster\n'
                'brother_Dinis: Im_gay_228'
            ),
            'connect geys.com': 'True'
        }

    def level2(self):
        while self.start:
            print('Ваша задача — украсть пароль Админа. Оплата 2000 долларов. '
                  'Как только вы украли пароль, пропишите его в командную строку.')
            user_command = input(self.directory)

            if user_command in self.command:
                print(self.command[user_command])

                # Проверка на правильный пароль
                if user_command == 'sudo connect main_backdor':
                    password_input = input("Введите пароль администратора: ")
                    if password_input == 'Rzk_Json123':
                        print('Проверка....')
                        time.sleep(3)
                        print('Успешно! Пароль украден.')
                        Menu(2000, 1)  # Предполагается, что Menu - это другой класс/функция
                        break
                    else:
                        print('Неверный пароль. Попробуйте снова.')
            else:
                print('Неизвестная команда. Попробуйте еще раз.')



start = HackPC(True)
start.level2()