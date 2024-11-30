# main.py
from deastole import Deastole

def run_process(start: bool):
    destole_instance = Deastole(start)
    destole_instance.start_main = True

    while destole_instance.start_main:
        destole_instance.main_start()

if __name__ == '__main__':
    def start_main(star:bool):
        run_process(star\