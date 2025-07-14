import json
import psycopg2
import os


class JsonToPsql:
    """Класс для работы с данными JSON и PostgreSQL."""

    def __init__(self):
        """Инициализация атрибутов и подключения к базе данных."""
        self.data = {}  # Словарь для хранения данных
        self.path_to_json = ''  # Путь к JSON-файлу
        self.connection = None  # Соединение с базой данных
        self.cursor = None  # Курсор для выполнения SQL-запросов

    def connect(self):
        """Подключение к базе данных PostgreSQL."""
        self.connection = psycopg2.connect(user='username',
                                           password='****',  # Заменено на ****
                                           host='localhost',
                                           port='5432',
                                           database='postgres')
        self.cursor = self.connection.cursor()  # Создание курсора

    def create_table(self):
        """Создание таблицы в базе данных, если она не существует."""
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS json_info(id BIGSERIAL PRIMARY KEY, \"user\" varchar(255), age int)")

    def close_connection(self):
        """Закрытие соединения с базой данных."""
        if self.cursor:
            self.cursor.close()  # Закрытие курсора
        if self.connection:
            self.connection.close()  # Закрытие соединения
        print("Соединение с базой данных закрыто.")

    def set_value(self):
        """Запрашивает путь к JSON-файлу у пользователя."""
        self.path_to_json = input('Enter path to json file: ')

    def json_read(self):
        """Чтение данных из JSON-файла и добавление их в базу данных."""
        if os.path.exists(self.path_to_json):  # Проверка существования файла
            with open(self.path_to_json, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Чтение данных из файла
                user = data['name']  # Извлечение имени пользователя
                age = data['age']  # Извлечение возраста пользователя
                self.add_info(user, age)  # Добавление информации в базу данных
        else:
            print('Ошибка: такого файла нет!!')  # Сообщение об ошибке

    def add_info(self, user, age):
        """Добавление информации о пользователе в базу данных."""
        self.cursor.execute("INSERT INTO json_info (\"user\", age) VALUES (%s, %s)", (user, age))
        self.connection.commit()  # Подтверждение изменений в базе данных
        print('Данные успешно добавлены.')  # Уведомление об успешном добавлении

    def run_for_JsonToPsql(self):
        """Запуск процесса работы с JSON и PostgreSQL."""
        self.connect()  # Подключение к базе данных
        self.create_table()  # Создание таблицы
        self.set_value()  # Запрос пути к JSON-файлу
        self.json_read()  # Чтение данных из JSON-файла
        self.close_connection()  # Закрытие соединения


class PsqlToJson(JsonToPsql):
    """Класс для извлечения данных из PostgreSQL и записи их в JSON."""

    def add_info_in_json(self):
        """Извлечение информации из базы данных и запись её в JSON-файл."""
        self.cursor.execute('SELECT "user", age FROM json_info')  # Запрос на извлечение данных
        results = self.cursor.fetchall()  # Получение всех записей

        user_and_age = [{'name': result[0], 'age': result[1]} for result in results]  # Формирование списка словарей

        self.set_value()  # Запрос пути к JSON-файлу

        if os.path.exists(self.path_to_json):  # Проверка существования файла
            with open(self.path_to_json, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Чтение существующих данных из файла
        else:
            data = []  # Если файл не существует, создаем пустой список

        data.extend(user_and_age)  # Добавление новых записей в список

        with open(self.path_to_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # Запись обновленных данных в файл

        print('Данные были добавлены в JSON!')  # Уведомление об успешном добавлении

    def run_PsqlToJson(self):
        """Запуск процесса извлечения данных из PostgreSQL и записи их в JSON."""
        self.connect()  # Подключение к базе данных
        self.create_table()  # Создание таблицы (если необходимо)
        self.add_info_in_json()  # Извлечение информации и запись её в JSON
        self.close_connection()  # Закрытие соединения


class MainRun(PsqlToJson):
    """Класс для управления выбором режима работы программы."""

    def run(self, choice: str):
        """Запуск соответствующего процесса в зависимости от выбора пользователя."""
        if choice == '1':
            print('Вы выбрали запись имени и лет из .json в psql')
            self.run_for_JsonToPsql()  # Запуск записи из JSON в PostgreSQL
        elif choice == '2':
            print('Вы выбрали запись в json из psql')
            self.run_PsqlToJson()  # Запуск записи из PostgreSQL в JSON
        else:
            print("Неверный выбор.")  # Сообщение об ошибке выбора

    def choice(self):
        """Запрос выбора режима работы у пользователя."""
        print('1. Запись имени и лет из .json в psql')
        print('2. Запись в json имени и лет из psql')
        return input('Выберите режим: ')  # Возврат выбора пользователя


def main():
    """Основная функция для запуска программы."""
    Start = MainRun()  # Создание экземпляра класса MainRun
    user_choice = Start.choice()  # Получаем выбор пользователя
    Start.run(user_choice)  # Передаем выбор в метод run()


if __name__ == '__main__':
    main()  # Запуск основной функции.
