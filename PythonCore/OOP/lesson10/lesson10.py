import random


def main():
    class Random_number:
        def __init__(self,random_d:int,much:int):
            self.random_number_d = random_d

            self.much = much
            self.index = self.much
            pass
        def __iter__(self):
            return self

        def __next__(self):
            if self.index == 0 :
                raise StopIteration

            else :
                n = random.randint(1,self.random_number_d)
                self.index -=1
                return n


    rand = Random_number(1000000,1000000)
    for number in rand:
        print(number)







if __name__ == '__main__':
    main()
