from PythonCore.megaprojects.hack_game.scr.menu import Menu


class Command:
    def __init__(self,start):
        self.start = start
        self.command = {''
            'netspy':'Обнаружено устройство с именем : Iphone 15 Pro '
            ,'sudo hack Iphone 15 Pro': ' Устройство успешно взломано ',}
        self.balance = 0

    def hack(self):
        while self.start == True :
            user_command =  input('/hone/hacker228/kali/hack/bin/command:').strip()
            if user_command in self.command:
                print(self.command[user_command])
                if user_command == 'sudo hack Iphone 15 Pro':
                    print('Вы взломали Iphone !Так держать !Пароль от google:qwery123')
                    print(f'Твой баланс :{self.balance + 1000} Долларов')
                    menu = Menu(1,self.balance)
                    menu.func()
                    self.start = False
            else :
                print('Команда не известна ')

def run_process(start:bool):
    terminal = Command(start)
    terminal.hack()


run_process(True)






