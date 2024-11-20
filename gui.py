import customtkinter
import threading
import time

class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('heart')

        self.button = customtkinter.CTkButton(
            self,
            text='End',
            command=self.test
        )
        self.button.place(x=600, y=1)

        self.project_description = customtkinter.CTkTextbox(
            master=self,
            width=400,
            corner_radius=2,
            state='normal'
        )
        self.project_description.insert('0.0', 'Description here')
        self.project_description.configure(state='disabled')
        self.project_description.place(x=1, y=1)

        self.text = customtkinter.CTkLabel(
            self,
            text='Heart pressure volume'
        )
        self.text.place(x=33, y=270)

        self.slider = customtkinter.CTkSlider(
            self,
            from_=0,
            to=100
        )
        self.slider.place(x=1, y=300)

        self.switch_var1 = customtkinter.StringVar(value="on")
        self.switch_var2 = customtkinter.StringVar(value="on")
        self.switch_var3 = customtkinter.StringVar(value="on")

        self.switch_1 = customtkinter.CTkSwitch(
            self,
            text='deabet',
            command=self.switch1,
            variable=self.switch_var1
        )
        self.switch_1.place(x=1, y=350)

        self.switch_2 = customtkinter.CTkSwitch(
            self,
            text='heart failure',
            command=self.switch2,
            variable=self.switch_var2
        )
        self.switch_2.place(x=1, y=375)

        self.switch_3 = customtkinter.CTkSwitch(
            self,
            text='old heart',
            command=self.switch3,
            variable=self.switch_var3
        )
        self.switch_3.place(x=1, y=400)

        self.status = True
        self.switch_value = None

        self.gender = 'Male'
        self.gender_switch = customtkinter.CTkSwitch(
            self,
            text=f'Gender is {self.gender}',
            command=self.gender_switch
        )

        self.gender_switch.place(x=1, y=450)


    def gender_switch(self):
        if self.gender == "Male":
            self.gender = "Female"
            self.gender_switch.configure(text=f'Gender is {self.gender}')
        else:
            self.gender = "Male"
            self.gender_switch.configure(text=f'Gender is {self.gender}')



    def switch1(self):
        pass

    def switch2(self):
        pass

    def switch3(self):
        pass

    def test(self):
        print(self.switch_value)

    def slider_updating_thread(self):
        self.status = True
        thread = threading.Thread(target=self.updater)
        thread.start()

    def updater(self):
        while self.status:
            self.switch_value = self.slider.get()
            time.sleep(0.2)

    def stop_slider_update_thread(self):
        self.status = False

    def close(self):
        self.status = False
        self.destroy()

app = Root()
app.slider_updating_thread()
app.mainloop()
