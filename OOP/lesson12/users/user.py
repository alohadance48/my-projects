from Mickhanika import Room



def main():
    class User :
        def user(self):
            # Запрос данных у пользователя
            width = float(input("Введите ширину комнаты (в метрах): "))
            length = float(input("Введите длину комнаты (в метрах): "))
            height = float(input("Введите высоту комнаты (в метрах): "))

            room = Room(width,length,height)


            while True:
                add_more = input("Хотите добавить окно или дверь? (да/нет): ").strip().lower()
                if add_more == 'да':
                    w = float(input("Введите ширину окна/двери (в метрах): "))
                    h = float(input("Введите высоту окна/двери (в метрах): "))
                    room.add_wd(w, h)
                else:
                    break

            print(f"Площадь оклеиваемой поверхности: {room.work_surface():.2f} кв.м")

            roll_width = float(input("Введите ширину рулона обоев (в метрах): "))
            roll_length = float(input("Введите длину рулона обоев (в метрах): "))

            rolls = room.rolls_needed(roll_width, roll_length)
            print(f"Необходимое количество рулонов: {rolls}")
    start = User()
    start.user()

    pass


if __name__ == '__main__':
    main()
