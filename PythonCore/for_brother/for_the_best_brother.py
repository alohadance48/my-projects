import time


def main():
    time.sleep(2)
    print('С Новым Годом, дорогой брат! Хочу сказать тебе спасибо за поддержку, помощь, советы. И это для тебя:')

    class CongratulationStart:
        def __init__(self):
            self.word = 'Спасибо тебе, брат! С Новым Годом!'
            self.brother = 'лучший брат на свете!'
            self.index = 5
            self.spaces = '     '

    class CongratulationMain(CongratulationStart):
        def print_heart(self):
            heart_shape = [
                "   ♥♥♥♥♥♥♥♥♥♥   ",
                " ♥♥♥♥♥♥♥♥♥♥♥♥♥♥ ",
                " ♥♥♥♥  лучший  ♥♥ ",
                " ♥♥  брат на свете ♥♥ ",
                "   ♥♥  лучший брат ♥♥   ",
                "     ♥♥♥♥♥♥♥♥     "
            ]

            for line in heart_shape:
                print(line)
                time.sleep(0.5)

        def congratulation(self, start: bool):
            if start:
                print(self.word)
                modified_brother = self.spaces + self.brother
                print(modified_brother)

                for i in range(self.index):
                    time.sleep(0.5)
                    modified_brother = modified_brother.replace(' ', '', 1)
                    print(modified_brother)

                time.sleep(1)
                print('Продолжаем....')
                time.sleep(3)

                print("Теперь слово 'брат' в форме сердца:")
                self.print_heart()
                time.sleep(5)

                for _ in range(100):
                    time.sleep(0.2)
                    print('Ты самый лучший брат на свете!')

                print('Еще раз с Новым Годом! Спасибо за наставление на правильный путь!')

                print('public class NewYearGreeting {'
                      '    public static void main(String[] args) {'
                      '        System.out.println("С Новым Годом!");'
                      '    }'
                      '}')

    start = CongratulationMain()
    start.congratulation(True)


if __name__ == '__main__':
    main()
