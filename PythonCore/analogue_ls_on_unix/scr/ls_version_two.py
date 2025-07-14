import os


def main():
    '''Точка входа'''
    class Files:
        def __init__(self):
            self.dir = '/home/' + os.getlogin()

        def files_on_pc(self):
            '''Рекурсивный обход directory'''
            for root, dirs, files in os.walk(self.dir):
                if files:
                    print(files)

    Start = Files()
    Start.files_on_pc()
    pass


if __name__ == '__main__':
    main()
