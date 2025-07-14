import os
import threading
import requests


def main():
    class FileManager:
        """
        Класс для управления файлами: сортировка, переименование и удаление.

        Атрибуты:
            dit (str): Текущая рабочая директория.
            user (str): Имя пользователя.
            all_file (list): Список всех файлов в текущей директории.
        """
        def __init__(self, base_dir=None):
            """
            Инициализирует объект FileManager с рабочей директорией и пользователем.

            Параметры:
                base_dir (str): Путь к директории (если не указан, используется текущая рабочаыя директория).
            """
            self.dit = base_dir or os.getcwd()  # текущая рабочая директория, если не указано
            self.user = os.getlogin()  # имя пользователя
            self.all_file = os.listdir(self.dit)  # все файлы в текущей директории

        def sort_file(self):
            """
            Сортирует файлы в директории по расширению и перемещает их в соответствующие папки.
            """
            print('Вы выбрали сортировку файлов')
            dir = input('Введите путь к директории: ')
            if not os.path.isdir(dir):
                print("Ошибка: Директория не найдена.")
                return

            os.chdir(dir)
            extensions = input("Введите расширения файлов через запятую (например, .txt,.jpg): ").split(',')
            extensions = [ext.strip().lower() for ext in extensions]

            for filename in os.listdir(dir):
                file_path = os.path.join(dir, filename)
                if os.path.isfile(file_path):
                    file_extension = os.path.splitext(filename)[1].lower()
                    if file_extension in extensions:
                        extension_folder = os.path.join(dir, file_extension[1:])
                        os.makedirs(extension_folder, exist_ok=True)
                        new_file_path = os.path.join(extension_folder, filename)
                        os.rename(file_path, new_file_path)
                        print(f"Перемещен файл: {filename} в {extension_folder}")

        def rename(self):
            """
            Переименовывает все файлы в директории, добавляя к их именам цифры.
            """
            name = input('Название файла (к названию будет добавляться цифра): ')
            files = os.listdir(self.dit)
            counter = 1

            for file in files:
                old_file_path = os.path.join(self.dit, file)
                if os.path.isfile(old_file_path):
                    new_name = f"{name}_{counter}{os.path.splitext(file)[1]}"
                    new_file_path = os.path.join(self.dit, new_name)
                    os.rename(old_file_path, new_file_path)
                    print(f"Файл {file} переименован в {new_name}")
                    counter += 1
        def delete(self):
            """
            Удаляет файлы в директории. Можно выбрать удаление по имени или расширению.
            """
            print('1. Удаление файла по имени.')
            print('2. Удаление по расширению.')
            choice = self.get_input('Выберите режим: ', [1, 2])

            if choice == 1:
                file_delete = input('Введите имя файла (с расширением): ')
                try:
                    os.remove(file_delete)
                    print(f"Файл {file_delete} удален!")
                except FileNotFoundError:
                    print("Ошибка: Файл не найден.")
                except PermissionError:
                    print("Ошибка: Нет прав для удаления файла.")
            elif choice == 2:
                print('Вы выбрали удаление по расширению.')
                file_extension = input('Введите расширение (например, .txt): ').lower()

                for filename in os.listdir(self.dit):
                    file_path = os.path.join(self.dit, filename)
                    if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() == file_extension:
                        os.remove(file_path)
                        print(f"Файл {filename} с расширением {file_extension} удален!")
                print('Удаление завершено.')

        def get_input(self, prompt, valid_values):
            """
            Запрашивает ввод от пользователя и проверяет, что введено корректное значение.

            Параметры:
                prompt (str): Сообщение для запроса.
                valid_values (list): Список допустимых значений.

            Возвращает:
                int: Валидное значение, выбранное пользователем.
            """
            while True:
                try:
                    value = int(input(prompt))
                    if value in valid_values:
                        return value
                    else:
                        print(f"Ошибка: Введите одно из допустимых значений {valid_values}.")
                except ValueError:
                    print("Ошибка: Введите число.")

        def choice(self):
            """
            Предлагает пользователю выбрать действие: сортировка, переименование или удаление файлов.
            """
            print("Выберите действие:")
            print("1. Сортировка файлов по расширению")
            print("2. Переименование файлов")
            print("3. Удаление файлов")
            action = self.get_input("Введите номер действия: ", [1, 2, 3])

            if action == 1:
                self.sort_file()
            elif action == 2:
                self.rename()
            elif action == 3:
                self.delete()

    class Windows(FileManager):
        """
        Класс для работы с файлами в операционной системе Windows.

        Наследует функциональность FileManager. Можно добавлять специфические для Windows методы.
        """
        pass  # Windows-специфичные функции можно добавить сюда, если необходимо

    class Unix(FileManager):
        """
        Класс для работы с файлами в операционной системе Unix.

        Наследует функциональность FileManager и проверку прав администратора.
        """
        def __init__(self, base_dir=None):
            """
            Инициализирует объект Unix и проверяет, имеются ли права администратора.

            Параметры:
                base_dir (str): Путь к директории (если не указан, используется текущая рабочая директория).
            """
            super().__init__(base_dir)
            self.check_root_permissions()

        def check_root_permissions(self):
            """
            Проверяет, есть ли у пользователя права администратора для выполнения операций.
            """
            if os.geteuid() != 0:
                print("Предупреждение: Потребуются права администратора для некоторых операций.")
            else:
                print("Работа с правами администратора возможна.")

    class Test:
        """
        Класс для тестирования веб-ресурса путём отправки запросов в несколько потоков.

        Атрибуты:
            link (str): URL для тестирования.
            colvo (int): Количество запросов.
            th (int): Количество потоков для выполнения запросов.
            thread (list): Список потоков.
        """
        def __init__(self):
            self.link = input('Введите ссылку на сайт: ')
            self.colvo = int(input('Введите кол-во запросов на сайт: '))
            self.th = int(input('Введите кол-во потоков: '))
            self.thread = []

        def test(self):
            """
            Отправляет запросы на указанный URL и выводит статус ответа.
            """
            for i in range(self.colvo):
                try:
                    response = requests.get(self.link)
                    print(f"Request {i + 1} status: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при запросе: {e}")

        def start(self):
            """
            Запускает многопоточное выполнение тестирования.
            """
            for _ in range(self.th):
                th_1 = threading.Thread(target=self.test)
                self.thread.append(th_1)
                th_1.start()

        def end_for_test(self):
            """
            Ожидает завершения всех потоков.
            """
            for th in self.thread:
                th.join()

    class Start:
        """
        Класс для выбора режима работы программы (Windows или Unix).
        """
        def __init__(self):
            self.choice = self.get_input('Выберите режим (1 - Windows, 2 - Unix, 3 - Test for backend): ', [1, 2,3])

        def get_input(self, prompt, valid_values):
            """
            Запрашивает ввод от пользователя и проверяет, что введено корректное значение.

            Параметры:
                prompt (str): Сообщение для запроса.
                valid_values (list): Список допустимых значений.

            Возвращает:
                int: Валидное значение, выбранное пользователем.
            """
            while True:
                try:
                    value = int(input(prompt))
                    if value in valid_values:
                        return value
                    else:
                        print(f"Ошибка: Введите одно из допустимых значений {valid_values}.")
                except ValueError:
                    print("Ошибка: Введите число.")

        def start(self):
            """
            Запускает выбор режима и соответствующие действия.
            """
            if self.choice == 1:
                print('Вы выбрали режим Windows!')
                start_windows = Windows()
                start_windows.choice()
            elif self.choice == 2:
                print('Вы выбрали режим Unix!')
                start_unix = Unix()
                start_unix.choice()
            else :
                A = Test()
                A.test()

    start_app = Start()  # Создаем объект для начала работы программы
    start_app.start()  # Запускаем программу


if __name__ == '__main__':
    main()
