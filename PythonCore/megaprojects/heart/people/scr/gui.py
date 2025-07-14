import customtkinter
from user import User
from deastole import Deastole
from dead import heart_failure
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('Heart Simulation')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.info_label = customtkinter.CTkLabel(self, text='Введите данные для симуляции:')
        self.info_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        self.age_label = customtkinter.CTkLabel(self, text='Сколько лет организму:')
        self.age_label.grid(row=1, column=0, pady=5, padx=20, sticky="w")

        self.age_entry = customtkinter.CTkEntry(self, placeholder_text='Введите возраст')
        self.age_entry.grid(row=1, column=1, pady=5, padx=20, sticky="ew")

        self.fatigue_label = customtkinter.CTkLabel(self, text='Выберите нагрузку (от 0 до 100):')
        self.fatigue_label.grid(row=2, column=0, pady=5, padx=20, sticky="w")

        self.fatigue_slider = customtkinter.CTkSlider(self, from_=0, to=100, number_of_steps=100)
        self.fatigue_slider.set(50)
        self.fatigue_slider.grid(row=2, column=1, pady=5, padx=20, sticky="ew")

        self.defect_label = customtkinter.CTkLabel(self, text='Выберите дефект:')
        self.defect_label.grid(row=3, column=0, pady=5, padx=20, sticky="w")

        self.defect_options = ["No Defect", "Heart Failure", "Diabetes", "Ventricular Syndrome"]
        self.selected_defect = customtkinter.StringVar(value="No Defect")
        self.defect_radio_buttons = []
        for i, option in enumerate(self.defect_options):
            button = customtkinter.CTkRadioButton(self, text=option, variable=self.selected_defect, value=option)
            button.grid(row=4, column=i, pady=5, padx=20)

        self.start_button = customtkinter.CTkButton(self, text='Запустить симуляцию', command=self.start_simulation)
        self.start_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.result_label = customtkinter.CTkLabel(self, text='Процесс: Ожидание начала симуляции...')
        self.result_label.grid(row=6, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=7, column=0, columnspan=2, pady=20, sticky="ew")

        self.reset_button = customtkinter.CTkButton(self.button_frame, text="Сбросить нагрузку", command=self.reset_load)
        self.reset_button.pack(side="left", padx=10)

        self.reset_button.configure(state="disabled")

        self.simulation_thread = None
        self.timer_thread = None
        self.is_simulating = False
        self.is_load_reset = False

        # Для графика пульса
        self.pulse_data = []  # Массив для хранения данных пульса
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Пульс')
        self.ax.set_xlabel('Время')
        self.ax.set_ylabel('Пульс')
        self.ax.set_ylim(50, 120)  # Установим границы пульса
        self.line, = self.ax.plot([], [], lw=2)  # Линия пульса создается, но пока без данных

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=2, pady=20, sticky="nsew")

    def start_simulation(self):
        try:
            user_age = int(self.age_entry.get())
            fatigue = int(self.fatigue_slider.get())
            defect_type = self.selected_defect.get()

            if not (0 <= fatigue <= 100):
                raise ValueError("Fatigue should be between 0 and 100.")

            user = User(user_age)
            has_defect = defect_type != "No Defect"

            defect_message = f"Defect: {defect_type}" if has_defect else "No defects detected"
            self.result_label.configure(text=f"Simulation started.\n{defect_message}")

            self.reset_button.configure(state="normal")

            if self.simulation_thread is None or not self.simulation_thread.is_alive():
                self.is_simulating = True
                self.is_load_reset = False
                self.simulation_thread = threading.Thread(target=self.run_simulation, args=(defect_type,))
                self.simulation_thread.daemon = True
                self.simulation_thread.start()

        except ValueError as e:
            self.result_label.configure(text=f"Error: {str(e)}")

    def run_simulation(self, defect_type):
        deastole = Deastole(True, defect_type)
        deastole.set_time(2 if defect_type == "Heart Failure" else 1)

        while self.is_simulating:
            fatigue = self.fatigue_slider.get()
            self.timer_thread = heart_failure(fatigue, int(self.age_entry.get()), self, self.is_simulating)

            if self.is_load_reset:
                if self.timer_thread:
                    self.timer_thread.cancel()
                    self.timer_thread = None
                self.result_label.configure(text="Нагрузка сброшена!")
                break

            deastole.main_start(self.update_blood_status, self.update_pulse)
            time.sleep(1)

    def update_blood_status(self, status_text: str):
        self.result_label.configure(text=status_text)

    def update_pulse(self, pulse: int):
        # Добавление пульса в список
        self.pulse_data.append(pulse)

        # Ограничиваем количество точек на графике, чтобы он не выходил за пределы
        if len(self.pulse_data) > 100:
            self.pulse_data.pop(0)

        # Обновляем график
        self.line.set_xdata(range(len(self.pulse_data)))
        self.line.set_ydata(self.pulse_data)

        # Обновление графика в интерфейсе
        self.after(0, self.canvas.draw)  # Используем after() для безопасного обновления GUI

    def reset_load(self):
        self.is_load_reset = True
        self.result_label.configure(text="Нагрузка сброшена.")
        self.reset_button.configure(state="disabled")