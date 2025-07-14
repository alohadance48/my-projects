import os

class Sort_for_file:
    def __init__(self):
        self.direct = '/home/vlados/sort'

class Sort_for_file_main(Sort_for_file):
    def sort_file(self):
        py_files = [f for f in os.listdir(self.direct)
                    if os.path.isfile(os.path.join(self.direct, f)) and f.lower().endswith('.json')]
        if py_files:
            print('Найдены файлы!')
            for file in py_files:
                souce = os.path.join(self.direct,file)
                desrination_path = os.path.join(os.path.expanduser('~/алгоритмы'),file)
                os.rename(souce,desrination_path)
                print(f'Файлы были перемецины в {desrination_path}')
                print('Файлы которф там находятся :')
                os.chdir('/home/vlados/python_os')
                print(os.popen('ls').read())
        else :
            print('Таких файлов нет')

start = Sort_for_file_main()
start.sort_file()
