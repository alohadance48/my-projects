import random

def main():
    class Michanika:
        def __init__(self):
            self.task_on_nigh = ['git', 'sql']
            self.start = True

        def add(self, task):
            self.task_on_nigh.append(task)

        def dell(self, index: int):
            if 0 <= index < len(self.task_on_nigh):
                self.task_on_nigh.pop(index)
            else:
                print("Ошибка: индекс вне диапазона.")

        def result(self):
            return self.task_on_nigh

        def rand_task(self):
            return random.choice(self.task_on_nigh) if self.task_on_nigh else None

    class ForUser(Michanika):
        def __init__(self):
            super().__init__()
            self.afk_mode = False

        def afk(self):
            if self.afk_mode:
                print('Вы в AFK режиме!')
                user_input = input('Введите "1" для выхода из AFK режима: ')
                if user_input == '1':
                    print('Вы вышли из AFK режима!')
                    self.afk_mode = False
                    self.main_task()
            else:
                print('Вы не в AFK режиме.')

        def main_task(self):
            while self.start:
                print('Наш функционал:')
                print('1. Просмотр задач')
                print('2. Добавление задач')
                print('3. Удаление задач')
                print('4. Рандомная задача из вашего списка')
                print('5. Режим AFK')
                print('6. Выход')

                choice = int(input('Выберите функцию: '))
                if choice == 1:
                    print('Ваши задачи:', self.result())
                elif choice == 2:
                    task = input('Введите новую задачу: ')
                    self.add(task)
                    print(f'Задача "{task}" добавлена.')
                elif choice == 3:
                    index = int(input('Введите индекс задачи для удаления: '))
                    self.dell(index)
                    print(f'Задача с индексом {index} удалена.')
                elif choice == 4:
                    task = self.rand_task()
                    if task:
                        print(f'Случайная задача: {task}')
                    else:
                        print('Список задач пуст.')
                elif choice == 5:
                    self.afk_mode = True
                    self.afk()
                elif choice == 6:
                    print("Выход из программы.")
                    self.start = False
                else:
                    print("Некорректный выбор, попробуйте снова.")

    # Создаем экземпляр класса ForUser и запускаем основную задачу
    user_instance = ForUser()
    user_instance.main_task()

if __name__ == '__main__':
    main()