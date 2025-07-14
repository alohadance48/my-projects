import threading
import requests

def main():
    class Get:
        def __init__(self):
            self.link = 'https://www.google.com/'
            self.threads = []


        def get_main(self):
            for _ in range(2):

                print('hi')

        def thread(self):
            for _ in range(5):
                self.thread = threading.Thread(target=self.get_main())
                self.threads.append(self.thread)
                self.thread.start()

        def end(self):
            for self.thread in self.threads:
                self.thread.join()
                print('Все потоки завершины.')

    get_m = Get()
    get_m.thread()
    get_m.end()
    pass

if __name__ == '__main__':
    main()