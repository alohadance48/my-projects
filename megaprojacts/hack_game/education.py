#education

import time
from OS_one import run_process




def main():
    class Education:
        def __init__(self):
            self.prolog = ('Я Леша JS C Плюс-Пслюсович бывший наркоман и гениальный хакер'
                           'взламываю системы и на полученные деньги от взлома покупаю лекарства !'
                           'Меня уже как 3 года ищет FBI. ')
            self.all_command = ('В игре есть список команд.Про все вы узнаете в ходе игры , '
                                'вот первые команды для нашей OS: netspy - ищет устройства подключенные к сети '
                                'sudo hack название устройства - ломает это устройство ')

        def start_game(self,start:bool):
            print(self.prolog)
            print(self.all_command)
            time.sleep(5)

            start = True
            if start == True :
                run_process(True)
            else :
                pass

    tst = Education()
    tst.start_game(True)



if __name__ == '__main__':
    main()
