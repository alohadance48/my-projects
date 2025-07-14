import psycopg2
import json
import os

def main():
    class Registration:
        def __init__(self):
            self.login = None
            self.password = None
            self.connection = None
            self.path_to_json = 'path_to_json'
            self.date = []

        def connect(self):
            '''Метод для подключения к базе данных.'''
            self.connection = psycopg2.connect(user = 'username',
                                               password = '******',
                                               host = '127.0.0.1',
                                               port = '5432',
                                               database = 'postgres'
            )
            self.cursor = self.connection.cursor() #Создание экземпляра cursor


        def create_tables(self):
            '''Метод для создания таблицы в psql'''
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (id BIGSERIAL PRIMARY KEY,
            login VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL,email VARCHAR(255) NOT NULL)''')
            self.connection.commit() #Подтверждение запроса

        def login_back(self):
            '''Метод для авторизации и регистрации'''
            self.login = input('Введите свой логи :')
            self.password = input('Введите свой пароль :')
            self.email = input('Введите свой email :')


        def add_info_in_table(self):
            '''Метод для добавления данных в таблицу(он только для регистрации)'''
            self.cursor.execute('''INSERT INTO users (login, password, email) values (%s,%s,%s)''',
                                (self.login, self.password, self.email))

            self.connection.commit() # Подтверждение изменений

        def info_in_json(self):
            '''Метод для создания шаблона данных для .json'''
            self.login_and_password = [{'user': self.login, 'password': self.password, 'email': self.email}]


        def __del__(self):
            '''Метод отключения от БД'''
            self.connection.close()


        def add_info_in_json(self):
            '''Метод добавления данных в json'''
            if os.path.isfile(self.path_to_json): # Проверка на наличие такого файла в директории
                with open(self.path_to_json, 'r',encoding='utf-8') as f: # Если такой файл есть, то он открывается в режиме чтения
                    self.date = json.load(f) # Получение предыдущий информации
            else :
                os.mkdir(self.path_to_json) # Если нет такого файла , то он создается
                self.date  = [] # Создание списка для будущих логов

            self.date.append(self.login_and_password) #Добавление логов в list
            with open(self.path_to_json, 'w',encoding='utf-8') as f:#Открытие файла в режиме write
                json.dump(self.date, f,ensure_ascii=False,indent=4)#Добавление логов
                f.close()# Закрытие файла


        def run_for_login(self):
            ''' Метод для запуска класса Регистрации '''
            self.connect() #Метод для подключения к БД
            self.create_tables()#Метод создания таблицы
            self.login_back()#Метод запросов информации об аккаунте
            self.add_info_in_table() # Метод для добавления инфы в таблицу
            self.__del__() # Метод отключения от БД
            self.info_in_json() #Метод для создания шаблона для .json
            self.add_info_in_json() #Метод добавления инфы в .json

    class LoginInAccount(Registration):
        '''Класс входа в аккаунт '''
        def login_in_account(self):
            '''Метод для подключения к БД и запроса инфы об аккаунте '''
            self.login_back() #метод логина
            self.connect() #метод подключения

        def examination(self):
            '''Метод сравнения данных из БД с данными user'''
            self.cursor.execute('SELECT login,password,email From users where email = %s ',self.email) # Выполняем запрос
            info = self.cursor.fetchall() #Получаем данные из таблицы
            if info:
                if info[0] == self.login and info[1] == self.password and info[2] == self.email: # Проверка данных
                    print('Вы успешно авторизовались!')
            else :
                print('Данные введены не правильно!')
                self.__del__() #Отключение от БД


        def run_for_account(self):
            self.login_in_account() #Метод для запуска Бд и запрос данных
            self.examination() #Метод проверки данных

    class Choice(Registration,LoginInAccount):
        '''Метод выбора режима '''
        def choice(self):
            choice = int(input('Выберите режим:'))
            if choice == 1:
                print('Вы выбрали вход в аккаунт')
                self.run_for_account()
            else :
                print('Вы выбрали создание нового аккаунта ')
                self.run_for_login()

    Start = Choice() #Экземпляр класса Choice
    Start.choice() #Метод класса Choice



if __name__ == '__main__':
    main()
