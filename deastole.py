import time




def main(): # вход
    #Родительский класс
    class Destole_main:
        #Определение начальных значений для статусов: крови, старта программы ( start_for_main_start) и, стыковочного старта (start).
        def __init__(self, start: bool):
            if start == True :
                self.index = 0
                self.start = False
                self.start_for_main_start = start
                self.blood = False
            else:
                print('Смерть. Симулиция оконченна')
                self.index = 0
                self.start = False
                self.start_for_main_start = False
                self.blood = False

            pass
        #Функция диастолы (расслабление мышцы)
        def deastole(self):
            time.sleep(2)
            print('Расслобление ')
            print('Выброс крови в организм')
            self.blood = True # Стыковочная переменная
            test(self.blood)
            print(self.blood)
            '''Каждые 2 секунды происходит переопределение переменной (blood) на (True начинается процесс). 
            deastole - стыковочный метод, если какой-то модуль умышленно выйдет из
            строя , значение blood определится на False причем станет статичной (больше не измениться в текущей симуляции ) 
            ( смотри модуль Dead) и , симуляция остановиться  , тебя  перекинет в главной меню (смотри модуль menu). '''
            pass
        #Функция систолы (расслабление мышцы)
        def sistole(self):
            time.sleep(2)
            print('Напрежение')
            print('Выброс прекращен')
            self.blood = False# Как я и говорил: переопределение.
            test(self.blood)
            print(self.blood)

            '''Каждые 2 секунды процесс прекращается . Значение переменной (blood) = False.'''
            pass
    #Дочерний класс ( наследование от Deastole_main)
    class Deastole(Destole_main):
        def main_start(self):
            while self.start_for_main_start:
                self.index += 1
                if self.index == 1:
                    self.deastole()
                else:
                    self.sistole()
                    self.index = 0
        '''Запуск всех процессов через цикл while , Если объект класса Deastole_main(start_for_main_start) будет False
        у нас ничего не запуститься . Счетчик индекc будет сбрасываться каждые 4 секунды( столько занимают реального 
        времени эти два процесса).Это один из основных методов(к нему подключены все модули.После чего он
        передаст все значения в класс контейнер, из которой передаст все в модуль info который выведет всю 
        информацию в графичском интерфейсе ).'''

    class for_info:
        def __init__(self,status:True):
            self.status_blood = status
        def info(self):
            pass
        '''Это класс контейнер.Из него идет передача в модуль info (он является модулем - контейнером).'''



    start = Deastole(start=True)# Создание экземпляра
    start.main_start()# Вызов метода




    pass


if __name__ == '__main__': # __name__ = __main__ ( это точка входа в программу )
    main()
    '''Вызов main() , после чего вызывается метод ,,main_start(),,.'''
