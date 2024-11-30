import time
from pynput import keyboard

class Deastole:
    def __init__(self):
        self.state = ''
        self.main_time = time.time()
        self.running = False

    def systole(self):
        self.state = 'Систола'
        print('Процесс систолы')

    def diastole(self):
        self.state = 'Диастола'
        print('Процесс диастолы')

    def main_process(self):
        self.running = True
        self.main_time = time.time()
        while self.running:
            start_time = time.time() - self.main_time
            if int(start_time) % 4 < 2:
                self.systole()
            else:
                self.diastole()
            time.sleep(0.5)

    def stop(self):
        self.running = False

def on_press(key):
    if key == keyboard.Key.delete:
        print('Завершение программы.')
        listener.stop()
        return False
    elif hasattr(key, 'char') and key.char == 'h':
        print("Нажата клавиша 'h'. Процесс продолжается.")
        if not heart.running:
            heart.main_process()

def on_release(key):
    if key == keyboard.Key.esc:
        print('Выход из программы.')
        return False

def main():
    global heart, listener
    heart = Deastole()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Симуляция остановлена.')
    finally:
        listener.stop()

if __name__ == '__main__':
    main()