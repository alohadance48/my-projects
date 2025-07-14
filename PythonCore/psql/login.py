import os
import json
import psycopg2


class LoginAndMainInfo:
    """Класс для получения и хранения информации о пользователе."""

    def __init__(self):
        """Инициализация атрибутов пользователя и пути к файлу логов и формата подключения к базе данных."""
        self.login = ''
        self.password = ''
        self.age = ''
        self.message = ''
        self.path = '/PythonCore/json_projects/logs/date.json'
        self.date = {}
        self.connection = psycopg2.connect(user='vlados',
                                           password='Rl_kL192#',
                                           host='127.0.0.1',
                                           port='5432',
                                           database='postgres')

    def create_table(self):
        """Создание таблицы и выполнение запросы """
        self.cursor = self.connection.cursor()
        table = """CREATE TABLE IF NOT EXISTS users ( id BIGSERIAL PRIMARY KEY,
                                                        first_name varchar(255) not null,
                                                        last_name varchar(255) not null,
                                                        email varchar(255) not null unique,
                                                        massage text not null);"""
        self.cursor.execute(table)
        self.connection.commit()

        pass

    def get_login_info(self):
        """Запрашивает у пользователя логин, пароль и возраст."""
        self.login = input('Enter your login: ')
        self.password = input('Enter your password: ')
        self.age = input('Enter your age: ')

    def send_message(self):
        """Запрашивает у пользователя сообщение."""
        self.message = input('Enter your message: ')

    def add_info_in_table(self):
        self.cursor.execute("INSERT INTO users (first_name, last_name, email, massage) values (%s, %s, %s, %s);",
                            (self.login, self.password, self.age, self.message))
        print('Данные были добавлены!')
        self.connection.commit()


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
        """Запускает процесс получения информации от пользователя и записи логов и записи в таблицу."""
        self.get_login_info()
        self.send_message()
        self.set_value()
        self.logs()
        self.create_table()
        self.add_info_in_table()

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


def main():
    """Основная функция для запуска программы."""
    test = Logout()
    test.run()


if __name__ == '__main__':
    main()
