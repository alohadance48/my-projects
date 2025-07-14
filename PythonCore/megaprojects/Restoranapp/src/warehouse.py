import psycopg2

def main():
    class ConnectionAndCloseConnection:
        def connect(self):
            """Метод для подключения к базе данных."""
            try:
                connect = psycopg2.connect(
                    user='postgres',
                    password='<PASSWORD>',
                    host='localhost',
                    port='5432',
                    database='postgres'
                )
                self.cursor = connect.cursor()
            except psycopg2.Error as e:
                print(f'Ошибка подключения: {e}')

        def disconnect(self):
            """Метод для закрытия соединения с базой данных."""
            self.cursor.close()

    class WarehouseSearchProduct(ConnectionAndCloseConnection):
        def __init__(self):
            self.product = None

        def set_value(self):
            """Установить название продукта для поиска."""
            self.product = input('Введите название продукта: ')

        def search_product(self):
            """Метод для поиска товара на складе."""
            try:
                self.cursor.execute(
                    """SELECT * FROM products WHERE product = %s""",
                    (self.product,)
                )
                product_search = self.cursor.fetchall()
                print(f'Продукт найден: {product_search}')
            except psycopg2.Error as e:
                print(f'Ошибка: {e}')
            finally:
                self.disconnect()

    class AddNewProduct(ConnectionAndCloseConnection):
        def __init__(self):
            self.product = None

        def add_product(self):
            """Метод для добавления новых продуктов на склад."""
            try:
                product = input('Введите название нового продукта: ')
                price = int(input('Введите цену продукта: '))
                self.cursor.execute(
                    """INSERT INTO warehouser VALUES (%s, %s)""",
                    (product, price)
                )  # Запрос на добавление продукта
                self.cursor.connection.commit()
                print('Продукт успешно добавлен!')
            except psycopg2.Error as e:
                print(f'Ошибка: {e}')
            finally:
                self.disconnect()

    class DeleteProduct(ConnectionAndCloseConnection):
        def __init__(self):
            self.product = None

        def set_value(self):
            """Установить название продукта для удаления."""
            self.product = input('Введите название продукта: ')

        def delete_product(self):
            """Метод для удаления продукта со склада."""
            try:
                self.cursor.execute(
                    """DELETE FROM warehouser WHERE product = %s""",
                    (self.product,)
                )  # Запрос на удаление продукта
                self.cursor.connection.commit()
                print('Продукт успешно удалён!')
            except psycopg2.Error as e:
                print(f'Ошибка: {e}')
            finally:
                self.disconnect()


if __name__ == '__main__':
    main()
