import json
import os

def main():
    class Main:
        def __init__(self):
            self.data = {}
            self.login = input("Login: ")
            self.password = input("Password: ")
            self.age = int(input("Age: "))

        def run(self):
            self.data = {
                'name': self.login,
                'password': self.password,
                'age': self.age
            }

            # Путь к файлу
            log_file = '/PythonCore/json_projects/logs/data.json'


            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as file:
                    logs = json.load(file)
            else:
                logs = []


            logs.append(self.data)
            print(logs)

            with open(log_file, 'w', encoding='utf-8') as file:
                json.dump(logs, file, ensure_ascii=False, indent=4)

            print('Логи были записаны!')

    A = Main()
    A.run()

if __name__ == '__main__':
    main()
