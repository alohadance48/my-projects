import os

def main():
    class All_file:
        def __init__(self):
            self.all_files = []


        def get_all_files(self):
            command = input('')
            if command == 'ls':
                path = os.getcwd()
                os.chdir(path)
                for item in os.listdir('..'):
                    self.all_files.append(item)

                print(self.all_files)

    pass

    Start = All_file()
    Start.get_all_files()

if __name__ == '__main__':
    main()
