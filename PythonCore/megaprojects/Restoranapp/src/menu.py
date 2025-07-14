import psycopg2


def main():
    class ConnectPsql:
        def connect(self):
            try:
                connect = psycopg2.connect(
                    user = 'username',
                    host='localhost',
                    port = '5432',
                    dbname = 'dbname',
                    password = 'password'
                                           )
                self.cursor = connect.cursor()
            except psycopg2.Error as error:
                print(f'Ошибка при подключении:{error}')
                exit()

    class UpdateMenu(ConnectPsql):
        def __init__(self):
            self.price = None
            self.product = None
            self.menu = {'Продукт':self.product,'Цена':self.price}

        def __search_products_and_set_value(self):
            product = input('Введите имя продукта для поиска:')
            product_search = self.cursor.execute("select product from menu where product = %s; ", product)
            if product_search is None:
                self.product = input('Введите новое название продукта:')
                self.price = int(input('Введите новую цену:'))
            else :
                print('Такого товара нет !')
                pass

        def __update_menu(self):

            self.cursor.execute("update menu set price = %s where product = %s;", (self.price, self.product))
            self.cursor.commit()
            print('Товары были успешно обновлены!')

        def __close(self):
            self.cursor.close()

        def run (self):
            self.connect()
            self.__search_products_and_set_value()
            self.__update_menu()
            self.__close()

    class AddMenu(ConnectPsql):
        def __init__(self):
            self.price = None
            self.product = None


        def set_value(self):
            self.product = input('Введите название продукта :')
            self.price = int(input('Введите  цену для продукта:'))

        def __add_product(self):
            self.cursor.execute("select product from menu where product = %s; ", self.product)
            examination_product =  self.cursor.fetchall()
            if examination_product:
                print('Ошибка,такой продукт уже есть!')
            else :
                self.cursor.execute("insert into menu (product, price) values (%s, %s);", (self.product, self.price))
                self.cursor.commit()
                print('Продукты успешно были добавлены!')

        def __close(self):
            self.cursor.close()

        def run(self):
            self.connect()
            self.__add_product()
            self.__close()


    class DeleteMenu(ConnectPsql):
        def __init__(self):
            self.product = None



        def set_value(self):
            self.product = input('Введите имя продукта:')

        def __close(self):
            self.cursor.execute("delete from menu where product = %s",(self.product))
            self.cursor.commit()
            self.cursor.close()
            print('Продукт был успешно удален')

        def run(self):
            self.connect()
            self.set_value()
            self.__close()


    class AllMenu(ConnectPsql):
        def __init__(self):
            self.menu = None


        def set_value(self):
            self.cursor.execute('select * from menu;')
            self.menu = self.cursor.fetchall()
            print(f'Все продукты в меню:{self.menu}')

        def __close(self):
            self.cursor.close()

        def run(self):
            self.connect()
            self.set_value()
            self.__close()

    class ModeSelect:
        def __init__(self):
            self.Update = 1
            self.Add = 2
            self.Delete = 3
            self.all = 4

        def choice(self):
            print('Доступные режимы:')
            print('1.Обновление меню')
            print('2.Добавление нового продукта и цены')
            print('3.Удаление продукты и цены')
            print('4.Просмотр всего меню ')
            choice_mode = input('Выберите режим :')
            if choice_mode == '1':
                start = UpdateMenu()
                start.run()
            elif choice_mode == '2':
                start = AddMenu()
                start.run()
            elif choice_mode == '3':
                start = DeleteMenu()
                start.run()
            elif choice_mode == '4':
                start = AllMenu()
                start.run()
            else:
                print('Ошибка!')

    start = ModeSelect()
    start.choice()
    pass

def run():
    main()

