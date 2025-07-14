import os # Библиотека для работы с файлами
import re # Регулярные выражения
import json # Библиотека для работы с файлами в формате .json


def main():# Точка входа в программу.
    class FilAndMainInfo:
        '''Класс для поиска файлов и ключевых слов внутри этих файлов, так же класс заносит логи в формате .json'''
        def __init__(self): #Обозначение основных переменных
            self.path = ''
            self.filename = ''
            self.word = ''
            self.dir_for_logs =''
            self.log_main = {}

        def set_value(self):
            '''Метод для присваивания новых значений для переменных  '''
            self.filename = input('Введите имя файла:') # Новое значение для имени файла
            self.word = input('Введите слово или строку:') # Новое значение для ключевого слова
            self.dir_for_logs = input('Введите диррикторию для логов(укажите путь и имя файла:') #Путь к файлу с логами
            self.path = input('Введите путь к папке:')


        def search_a_file(self):
            '''Метод для поиска файла по его имени
            поиск будет происходить из /home/user.'''
            for root, dirs, files in os.walk(self.path):
                if self.filename in files:
                    self.path = root
                    print('Файл найден, его путь :',root)



        def search_for_a_text_in_file(self):
            '''Метод для поиска ключевых слов'''
            os.chdir(self.path)
            if os.path.isfile(self.filename): # Проверка есть ли такой файл по указанному пути.
                file_content = open(self.filename,'r') # Режим чтения при открытие файла
                content = file_content.read() # Получение текста в переменною
                pattern = rf'([^.?!]*\b{self.word}\b[^.?!]*[.?!])' #Ключевое слово и символы
                match = re.findall(pattern, content) #Поиск всех совпадений
                if match:
                    '''Если такие есть ,то создается шаблон для заноса в логи, формат - .json'''
                    print('Найдено совпадение:',match)
                    self.log_main = {'слово': self.word,
                                     'имя файла': self.filename,
                                     'путь':self.dir_for_logs,
                                     'совпадение:':match}

                else:
                    '''Обработка ошибок '''
                    print('Нет такого слова или строки!')
            else:
                print('Ошибка,нет такого файла по пути:', self.path)
                pass

        def logs(self):
            '''Метод для создания логов и заноса в файл.'''
            if os.path.exists(self.dir_for_logs): #Проверка на наличие такого файла
                '''Если есть такой файл , то он открывается в режиме чтения, и логи добавляются в список
                (это нужно для корректного заноса логов).'''
                with open(self.dir_for_logs,'r',encoding='utf-8') as f:
                    logs = json.load(f) # Тут добавляются все старые логи
            else :
                logs = [] #Если логов нету ,то у нас будет пустой список

            logs.append(self.log_main) #добавление логов в список

            with open(self.dir_for_logs,'w',encoding='utf-8') as f: #Открытие файла в режиме редактора
                json.dump(logs,f,ensure_ascii=False,indent=4) #Добавление новых логов
                print('Логи были добавлены')


        def run(self):
            '''Метод для запуска всех метод (он нужен для корректного запуска программы).'''
            self.set_value()#Метод присваивания
            self.search_a_file() #Метод поиска файла
            self.search_for_a_text_in_file() #Метод для поиска ключевых слов
            self.logs() #Метод создания логов

    start = FilAndMainInfo() #Экземпляр класса
    start.run() #Метод



if __name__ == '__main__':
    '''Запуск программы(по факту,в __main__ будет содержаться True , это будет выглядеть так : 
     if __name__ == True:'''
    main() #Запуск
