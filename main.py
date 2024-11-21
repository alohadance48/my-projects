# main.py
from deastole import Deastole
from tkinter import messagebox
from gui import Root

def run_process(start: bool, root: Root):
    destole_instance = Deastole(start, root)
    destole_instance.start_main = True

    while destole_instance.start_main:
        destole_instance.main_start()
        if not destole_instance.start_main:
            messagebox.showinfo("Симуляция завершена", "Вы погибли.")
            break

if __name__ == '__main__':
    app = Root()
    app.mainloop()