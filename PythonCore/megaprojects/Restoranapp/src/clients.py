import psycopg2

def main():
    class Connection:
        def __connect(self):
            try:
                connection = psycopg2.connect(host='localhost',
                                 port=5432,
                                 database='postgres',
                                 user='postgres',
                                 password='<PASSWORD>'
                                 )

                self.cursor = connection.cursor()
            except psycopg2.Error as error:
                print(error)


        def __disconnect(self):
            try:
                self.cursor.close()
            except psycopg2.Error as error:
                print(error)

    class Clients(Connection):
        def __init__(self):
            self.clients = []

        def set_value(self):
            print('Вы выбрали добавление нового клиента!')
            new_client = input('Enter client name: ')
            self.__add_clients(new_client)


        def __add_clients(self, client):
            self.clients.append(client)

        def __remove_client(self, client):
            print('Вы выбрали удаление клиента!')
            delete_client = input('Enter client name: ')
            self.__remove_client_Datebase(delete_client)

        def __add_client_in_datebase(self):
            try:
                self.__connect()
                for client in self.clients:
                    self.cursor.execute('BEGIN;')
                    self.cursor.execute('INSERT INTO clients (client_name) VALUES (%s);', (client,))
                    self.cursor.execute('COMMIT;')

                self.__disconnect()
            except psycopg2.Error as error:
                print('Ошибка при добавлении клиента:',error)
                self.__disconnect()

            finally:
                self.__disconnect()


        def __remove_client_Datebase(self, client):
            try:
                self.cursor.execute('BEGIN;')
                self.cursor.execute('DELETE FROM clients WHERE client_name = %s;', (client,))
                self.cursor.execute('COMMIT;')
                self.__disconnect()
                print('Вы успешно удалили клиента!')
            except psycopg2.Error as error:
                print('Ошибка при удаление клиента!',error)
            finally:
                self.__disconnect()

        def select_all_clients(self):
            try:
                self.__connect()
                self.cursor.execute('SELECT * FROM clients;')
                all_clients =  self.cursor.fetchall()
                self.__disconnect()
                print(all_clients)


            except psycopg2.Error as error:
                print(error)
                self.__disconnect()

            finally:
                self.__disconnect()


    class Choice(Connection,Clients):
        def choice(self):
            print('Вы выбрали управление базой данных клиентов!')
            print('Выберете функционал:')
            print('1.Создание нового клиента')
            print('2.Удаление клиента')
            print('3.Просмотр всех клиентов')
            choice = int(input('Сделайте выбор: '))
            try:
                match choice:
                    case 1:
                        self.set_value()
                        self.__add_client_in_datebase()
                    case 2:
                        self.__remove_client(choice)
                    case 3:
                        self.select_all_clients()
            except ValueError:
                print('Ошибка выбора!')



if __name__ == '__main__':
    main()
