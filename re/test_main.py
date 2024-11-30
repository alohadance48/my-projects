import requests
import time



def main():
    class Links:
        def __init__(self):
            self.google = 'https://www.google.com/'
            self.youtube = 'https://www.google.com/'  # Заменено на Google
            self.github = 'https://www.google.com/'   # Заменено на Google
            self.stackoverflow = 'https://www.jetbrains.com/ru-ru/youtrack/download/get_youtrack.html'  # Заменено на Google
            self.reddit = 'https://www.google.com/'  # Заменено на Google
            self.twitter = 'https://www.google.com/'  # Заменено на Google
            self.facebook = 'https://www.google.com/'  # Заменено на Google
            self.linkedin = 'https://www.google.com/'  # Заменено на Google
            self.instagram = 'https://www.google.com/'  # Заменено на Google
            self.wikipedia = 'https://www.google.com/'  # Заменено на Google
            self.list = [self.google, self.youtube, self.github, self.stackoverflow,
                         self.reddit, self.twitter, self.facebook,
                         self.linkedin, self.instagram, self.wikipedia]
            self.index = len(self.list)

    class TestLinks(Links):
        def choice_link(self):
            index = 0
            while index < self.index  :
                time.sleep(1)
                get = requests.get(self.list[index])
                if get.status_code == 200:
                    print(f'{self.list[index]}: Все окей. Код {get}')

                else:
                    print(f'{self.list[index]}: ошибка. Код:', get)
                index += 1

    test = TestLinks()
    test.choice_link()

if __name__ == '__main__':
    main()