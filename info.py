# info.py
import unittest


class Info:
    def deastole(self, status: bool) -> bool:
        print(f"Info: Blood status is now {'Deastole' if status else 'Sistole'}") #True
        print( True)

    def user_info(self, is_old: int,fatigue:int):
        print(f'Info:you old:{is_old}твоя нагрузка:{fatigue}') #True
        print( True)

    def defects(self, not_full_heart: bool, deabet: bool, olf: bool):
        print(True)

    def dead(self, start: bool): #True
        if start == True :
            print('Вы погибли')
        else :
            print('Вы выжили')

        print( True)

    def pulse(self, status: int):
        print(True)

    def end(self, end: bool):
        print(  True )


