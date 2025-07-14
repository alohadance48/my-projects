import os
import json


class LoginAndMainInfo:
    """Класс для получения и хранения информации о пользователе."""

    def __init__(self):
        """Инициализация атрибутов пользователя и пути к файлу логов."""
        self.login = ''
        self.password = ''
        self.age = ''
        self.message = ''
        self.path = os.getcwd() + '/date.json'
        self.date = {}

    def get_login_info(self):
        """Запрашивает у пользователя логин, пароль и возраст."""
        self.login = input('Enter your login: ')
        self.password = input('Enter your password: ')
        self.age = input('Enter your age: ')

    def send_message(self):
        """Запрашивает у пользователя сообщение."""
        self.message = input('Enter your message: ')


class Logout(LoginAndMainInfo):
    """Класс для обработки выхода и записи информации в логи."""

    def set_value(self):
        """Устанавливает значения атрибутов в словарь для записи в логи."""
        self.date = {
            'user': self.login,
            'password': self.password,
            'age': self.age,
            'message': self.message,
        }

    def run(self):
        """Запускает процесс получения информации от пользователя и записи логов."""
        self.get_login_info()
        self.send_message()
        self.set_value()
        self.logs()

    def logs(self):
        """Записывает информацию о пользователе в файл логов."""
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                logs = json.load(file)
        else:
            logs = []

        logs.append(self.date)

        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(logs, file, ensure_ascii=False, indent=4)

        print('Логи были добавлены!')
        print(self.path)

def main():
    """Основная функция для запуска программы."""
    test = Logout()
    test.run()


if __name__ == '__main__':
    main()
