import requests
from bs4 import BeautifulSoup
import csv
import re
import os
from datetime import datetime
import pytz
import mysql.connector
from mysql.connector import Error

# Настройки подключения к MySQL
db_config = {
    'host': 'localhost',
    'user': '1212',
    'password': '1212',
    'database': '1212'
}


def fetch_prices(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    # Поиск информации о товаре
    title_tag = soup.find('h1')
    price_block = soup.find('div', class_='price-block-1')
    verification_price_tag = soup.find('span', class_='verification-price')  # Обновите класс по вашему сайту

    if price_block:
        price_tag = price_block.find('span', class_='price')
    else:
        price_tag = None

    if title_tag and price_tag and verification_price_tag:
        title = title_tag.text.strip()
        price_text = price_tag.text.strip()
        price = re.findall(r'\d+[\d\s]*', price_text)
        price = ''.join(price).replace(' ', '') if price else 'N/A'

        verification_price_text = verification_price_tag.text.strip()
        verification_price = re.findall(r'\d+[\d\s]*', verification_price_text)
        verification_price = ''.join(verification_price).replace(' ', '') if verification_price else 'N/A'

        moscow_tz = pytz.timezone('Europe/Moscow')
        moscow_time = datetime.now(moscow_tz)
        formatted_time = moscow_time.strftime('%Y-%m-%d %H:%M:%S')

        products.append(
            {'title': title, 'verification_price': verification_price, 'price': price, 'time': formatted_time})
    else:
        print("Error parsing product information. Title, price, or verification price not found.")

    return products


def save_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Verification Price', 'Price', 'Time'])  # Обновленный заголовок
            for row in data:
                writer.writerow([row['title'], row['verification_price'], row['price'], row['time']])
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")


def load_from_csv(filename):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропуск заголовка
            return [{'title': row[0], 'verification_price': row[1], 'price': row[2], 'time': row[3]} for row in reader]
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
        return []
    except IndexError as e:
        print(f"Error parsing CSV file {filename}: {e}")
        return []


def compare_prices(old_prices, new_prices):
    old_dict = {item['title']: item for item in old_prices}
    changes = []
    for item in new_prices:
        title = item['title']
        old_item = old_dict.get(title)
        if old_item:
            if (old_item['price'] != item['price'] or
                    old_item['verification_price'] != item['verification_price']):
                changes.append({
                    'title': title,
                    'old_price': old_item['price'],
                    'new_price': item['price'],
                    'old_verification_price': old_item['verification_price'],
                    'new_verification_price': item['verification_price']
                })
    return changes


def connect_to_database(config):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Соединение с базой данных успешно установлено")
            return connection
    except Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None


def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        verification_price DECIMAL(10, 2),
        price DECIMAL(10, 2),
        time DATETIME
    )
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица создана или уже существует.")
    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        cursor.close()


def insert_data_from_csv_to_db(connection, csv_file_path):
    insert_query = """
    INSERT INTO products (title, verification_price, price, time)
    VALUES (%s, %s, %s, %s)
    """
    cursor = connection.cursor()
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Пропуск заголовка
            for row in csvreader:
                title, verification_price, price, time = row
                try:
                    cursor.execute(insert_query, (title, float(verification_price), float(price), time))
                except Error as e:
                    print(f"Ошибка вставки данных: {e}")
        connection.commit()
        print("Данные успешно вставлены в таблицу.")
    except Error as e:
        print(f"Ошибка при вставке данных: {e}")
    except Exception as ex:
        print(f"Ошибка при обработке файла: {ex}")
    finally:
        cursor.close()


def main():
    url = input('Введите ссылку: ')
    filename = 'prices.csv'

    # Получение новых цен
    new_prices = fetch_prices(url)

    if not new_prices:
        print("No new prices fetched.")
    else:
        # Загружаем старые цены
        old_prices = load_from_csv(filename)

        # Сравнение
        changes = compare_prices(old_prices, new_prices)

        # Сохранение новых данных в CSV
        save_to_csv(new_prices, filename)

        # Подключение к базе данных
        connection = connect_to_database(db_config)

        if connection:
            # Создание таблицы
            create_table(connection)

            # Вставка данных из CSV в базу данных
            insert_data_from_csv_to_db(connection, filename)

            # Закрытие соединения
            connection.close()

        # Вывод изменений в ценах
        if changes:
            print("Обнаружены изменения в ценах:")
            for change in changes:
                print(
                    f"Товар: {change['title']}, Старая цена: {change['old_price']}, Новая цена: {change['new_price']}, Старая цена поверки: {change['old_verification_price']}, Новая цена поверки: {change['new_verification_price']}")
        else:
            print("Изменений в ценах не обнаружено.")


if __name__ == "__main__":
    main()
