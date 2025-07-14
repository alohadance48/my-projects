from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import psycopg2
import base64
import os


class Search:
    def __init__(self):
        self.user_info = None
        self.text_1 = "Солнце светило ярко в тот летний день."
        self.text_2 = """
                    1. Страницы.html должны хранится в templates/DateBaseApp, ошибки.html в templates/Errors.
                    2. Страницы.css должны хранится в static/css, ошибки.css в static/Errors.
                    3. Страницы.js должны хранится в static/js, ошибки.js в static.js
                    4. Картинки.png должны хранится в static/png.
                    """
        self.key = os.urandom(32)  # Генерация случайного 256-битного ключа для AES

    def connect(self):
        """Подключение к базе данных PostgreSQL."""
        self.connect = psycopg2.connect(
            user='vladosl',
            password='RzkJh1#898',
            database='postgres_db',  # Используйте правильное название вашей базы данных
            host='127.0.0.1',
            port='5432'
        )
        self.cursor = self.connect.cursor()

    def encrypt(self, text):
        """Шифрует текст с использованием AES-256 в режиме CBC."""
        iv = os.urandom(16)  # Генерация случайного IV (инициализационного вектора)

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Дополняем текст, чтобы его длина была кратна блоку шифрования (16 байт для AES)
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(text.encode()) + padder.finalize()

        encrypted_text = encryptor.update(padded_data) + encryptor.finalize()

        # Возвращаем IV и зашифрованный текст, закодированные в base64
        return base64.b64encode(iv + encrypted_text).decode('utf-8')

    def decrypt(self, encrypted_text):
        """Расшифровывает текст с использованием AES-256 в режиме CBC."""
        encrypted_data = base64.b64decode(encrypted_text)
        iv = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_message) + decryptor.finalize()

        # Удаляем дополнение
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        original_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return original_data.decode()

    def add_encrypted_texts(self):
        """Создает таблицу в базе данных и добавляет зашифрованные тексты."""
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS info (id BIGSERIAL PRIMARY KEY, text VARCHAR(255) NOT NULL)''')
        encrypted_text_1 = self.encrypt(self.text_1)
        encrypted_text_2 = self.encrypt(self.text_2)

        self.cursor.execute("INSERT INTO info (text) VALUES (%s)", (encrypted_text_1,))
        self.cursor.execute("INSERT INTO info (text) VALUES (%s)", (encrypted_text_2,))

    def set_value(self):
        """Запрашивает текст от пользователя."""
        self.user_info = input('Enter your word or all text: ')

    def search(self):
        """Ищет в базе данных и расшифровывает данные."""
        search_term = self.user_info
        self.cursor.execute("SELECT * FROM info WHERE text LIKE %s", (f'%{search_term}%',))
        results = self.cursor.fetchall()

        for row in results:
            encrypted_text = row[1]
            print(f"Encrypted Text: {encrypted_text}")
            decrypted_text = self.decrypt(encrypted_text)
            print(f"Decrypted Text: {decrypted_text}")

    def close(self):
        """Закрывает соединение с базой данных."""
        self.cursor.close()
        self.connect.close()


def main():
    search_instance = Search()
    search_instance.connect()

    # Добавление зашифрованных данных в базу данных
    search_instance.add_encrypted_texts()  # Переименовали метод

    # Запрашиваем от пользователя слово или текст для поиска
    search_instance.set_value()

    # Поиск и расшифровка
    search_instance.search()

    # Закрытие соединения с базой данных
    search_instance.close()


if __name__ == '__main__':
    main()
