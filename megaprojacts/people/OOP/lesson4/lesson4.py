import time
import random



def main():
    class Characteristics:  # Родительский класс
        def __init__(self):
            list_chars = ['A', 'B', 'G', 'D', 'F', 'Q']
            self.id = str(random.randint(1, 10000)) + random.choice(list_chars) + str(random.randint(1, 1000)) + random.choice(list_chars)
            self.level = 1
            self.list_player = []
            self.list_player_one = []
            self.hero = 'gey'

        def on_the_heels(self, hero: bool = False):
            pass

        def level_up(self, module: bool = False):
            if module:
                self.level += 1

    class Hero(Characteristics):
        def __init__(self):
            super().__init__()

        def create_hero(self, number):
            for i in range(number):
                time.sleep(1)
                choice = random.randint(1, 2)
                if choice == 1:
                    self.list_player.append(self.hero)
                else:
                    self.list_player_one.append(self.hero)
                print(self.list_player, self.list_player_one)
                if len(self.list_player) > len(self.list_player_one):
                    self.level_up(True)
                else:
                    self.level_up(True)

    game = Hero()
    game.create_hero(10)


if __name__ == '__main__':
    main()
