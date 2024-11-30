import random



def main():
    class Random_number:
        def __init__(self):
            self.much = int(input('Ваше число :'))
            self.d = int(input('Ваш деапозон '))
            pass
        def main_rand_number(self):
            for i in range(self.much):
                yield random.randint(1,self.d)

    start = Random_number()
    for number in start.main_rand_number():
        print(number)


if __name__ == '__main__':
    main()
