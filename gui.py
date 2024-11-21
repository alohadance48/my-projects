# gui.py

import customtkinter

from user import DescriptionOfTheHeart


class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('Heart Simulation')

        self.info_label = customtkinter.CTkLabel(self, text='Введите данные для симуляции:')
        self.info_label.pack(pady=20)

        self.age_label = customtkinter.CTkLabel(self, text='Сколько лет организму:')
        self.age_label.pack(pady=5)
        self.age_entry = customtkinter.CTkEntry(self, placeholder_text='Введите возраст')
        self.age_entry.pack(pady=10)

        self.fatigue_label = customtkinter.CTkLabel(self, text='Твоя нагрузка (от 0 до 100):')
        self.fatigue_label.pack(pady=5)
        self.fatigue_entry = customtkinter.CTkEntry(self, placeholder_text='Введите нагрузку')
        self.fatigue_entry.pack(pady=10)

        self.gender_label = customtkinter.CTkLabel(self, text='Ваш пол:')
        self.gender_label.pack(pady=5)

        self.gender_switch = customtkinter.CTkSwitch(self, text='Мужской', command=self.toggle_gender)
        self.gender_switch.pack(pady=10)

        self.start_button = customtkinter.CTkButton(self, text='Запустить симуляцию', command=self.start_simulation)
        self.start_button.pack(pady=20)

        self.result_label = customtkinter.CTkLabel(self, text='')
        self.result_label.pack(pady=20)

        self.stop_entry = customtkinter.CTkButton(self, text='Сброс нагрузки', command=self.reset_load)
        self.stop_entry.pack(pady=10)

        self.gender = "Мужской"  # По умолчанию пол "Мужской"

    def toggle_gender(self):
        if self.gender == "Мужской":
            self.gender = 'Женский'
            self.gender_switch.configure(text='Женский')

        else:
            self.gender = "Мужской"
            self.gender_switch.configure(text='Мужской')

    def start_simulation(self):
        try:
            user_age = int(self.age_entry.get())
            fatigue = int(self.fatigue_entry.get())

            description = DescriptionOfTheHeart(user_age, fatigue, self.gender, self)
            description.paraments()
        except ValueError:
            self.result_label.configure(text='Пожалуйста, введите корректные данные.')


        self.info_label = customtkinter.CTkLabel(self, text="")
        self.info_label.pack(pady=20)


        self.reset_button = customtkinter.CTkButton(self, text="Сбросить нагрузку", command=self.reset_load)
        self.reset_button.pack(pady=20)

    def update_info(self, message):
        self.info_label.configure(text=message)

    def reset_load(self):
        presure_drop()
