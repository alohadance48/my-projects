import random
import time

def main ():
    class Warrior:
        def __init__(self):
            self.warrior_one_hp = 100
            self.warrior_two_hp = 100

        def attack(self):
            module = True
            while module == True :
                time.sleep(1)
                random_attack = random.randint(1,2)
                if random_attack == 1 :
                    self.warrior_two_hp -= 20
                    print('Ударил первый юнит , хп второго юнита :',self.warrior_two_hp)
                    print('хп первого юнита :',self.warrior_one_hp)
                else :
                    self.warrior_one_hp -= 20
                    print('Ударил второй юнит , хп первого  юнита :',self.warrior_one_hp)
                    print('хп второго юнита :',self.warrior_two_hp)
                if self.warrior_one_hp <= 0:
                    print('Победу одержал второй юнит')
                    module = False
                elif self.warrior_two_hp <=0 :
                    print('Победу одержал первый юнит')
                    module = False
    battle = Warrior()
    battle.attack()


    pass

if __name__ == '__main__':
    main()