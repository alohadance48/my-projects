import telebot
from telebot import types
import time
import math

TOKEN = ''  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

# Создание объекта для хранения данных (для обработки поэтапных запросов)
user_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message)

# Функция для отображения основного меню
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton("МКТ")
    item2 = types.KeyboardButton("Базовые задачи")
    item3 = types.KeyboardButton("Термодинамика")
    item4 = types.KeyboardButton("Цепи")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Привет! Выберите категорию для решения задачи:", reply_markup=markup)

# Обработчик выбора категории
@bot.message_handler(func=lambda message: message.text in ["МКТ", "Базовые задачи", "Термодинамика", "Цепи"])
def select_category(message):
    category = message.text
    if category == "Базовые задачи":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("Скорость")
        item2 = types.KeyboardButton("Время")
        item3 = types.KeyboardButton("Путь")
        item4 = types.KeyboardButton("Ускорение")
        item5 = types.KeyboardButton("Импульс")
        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(message.chat.id, "Выбери задачу, которую хочешь решить:", reply_markup=markup)
        user_data[message.chat.id] = {"category": "Базовые задачи"}
    elif category == "МКТ":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("Давление газа")
        item2 = types.KeyboardButton("Средняя скорость молекул")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Выбери задачу из категории МКТ:", reply_markup=markup)
        user_data[message.chat.id] = {"category": "МКТ"}
    elif category == "Термодинамика":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("Работа газа")
        markup.add(item1)
        bot.send_message(message.chat.id, "Выбери задачу из категории Термодинамика:", reply_markup=markup)
        user_data[message.chat.id] = {"category": "Термодинамика"}
    elif category == "Цепи":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("Сила тока в цепи")
        markup.add(item1)
        bot.send_message(message.chat.id, "Выбери задачу из категории Цепи:", reply_markup=markup)
        user_data[message.chat.id] = {"category": "Цепи"}

# Обработчик для базовых задач
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "Базовые задачи")
def basic_task(message):
    if message.text.lower() == "скорость":
        bot.send_message(message.chat.id, "Для расчета скорости мне нужны следующие данные:\n"
                                           "1. Путь (в метрах)\n"
                                           "2. Время (в секундах)\n"
                                           "Введите путь (в м):")
        user_data[message.chat.id] = {"task": "скорость"}
    elif message.text.lower() == "время":
        bot.send_message(message.chat.id, "Для расчета времени мне нужны следующие данные:\n"
                                           "1. Путь (в метрах)\n"
                                           "2. Скорость (в м/с)\n"
                                           "Введите путь (в м):")
        user_data[message.chat.id] = {"task": "время"}
    elif message.text.lower() == "путь":
        bot.send_message(message.chat.id, "Для расчета пути мне нужны следующие данные:\n"
                                           "1. Скорость (в м/с)\n"
                                           "2. Время (в секундах)\n"
                                           "Введите скорость (в м/с):")
        user_data[message.chat.id] = {"task": "путь"}
    elif message.text.lower() == "ускорение":
        bot.send_message(message.chat.id, "Для расчета ускорения мне нужны следующие данные:\n"
                                           "1. Изменение скорости (в м/с)\n"
                                           "2. Время (в секундах)\n"
                                           "Введите изменение скорости (в м/с):")
        user_data[message.chat.id] = {"task": "ускорение"}
    elif message.text.lower() == "импульс":
        bot.send_message(message.chat.id, "Для расчета импульса мне нужны следующие данные:\n"
                                           "1. Масса (в кг)\n"
                                           "2. Скорость (в м/с)\n"
                                           "Введите массу (в кг):")
        user_data[message.chat.id] = {"task": "импульс"}

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "МКТ")
def mkt(message):
    if message.text.lower() == "давление газа":
        bot.send_message(message.chat.id, "Для расчета давления газа нужны следующие данные:\n"
                                           "1. Количество вещества газа (моль, n)\n"
                                           "2. Температура газа (в Kельвинах, T)\n"
                                           "3. Объем газа (м³, V)"
                                           "Введите все переменные подряд в формате без запятых. Пример: 2 4 6")
        user_data[message.chat.id] = {"task": "давление газа"}
    elif message.text.lower() == "средняя скорость молекул":
        bot.send_message(message.chat.id, "Для расчета средней скорости молекул нужны следующие данные:\n"
                                           "1. Температура газа (в Kельвинах, T)\n"
                                           "2. Масса одной молекулы газа (кг, m)"
                                           "Введите все переменные подряд в формате без запятых. Пример: 2 4")
        user_data[message.chat.id] = {"task": "средняя скорость молекул"}

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "Термодинамика")
def thermodynamics(message):
    if message.text.lower() == "работа газа":
        bot.send_message(message.chat.id, "Для расчета работы газа нужны следующие данные:\n"
                                          "1. Давление газа (в Дж, P)\n"
                                          "2. Изменение объема газа (м³, ΔV)"
                                          "Введите все переменные подряд в формате без запятых. Пример: 2 4")
        user_data[message.chat.id] = {"task": "работа газа"}

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "Цепи")
def thermodynamics(message):
    if message.text.lower() == "сила тока в цепи":
        bot.send_message(message.chat.id, "Для расчета силы тока в цепи нужны следующие данные:\n"
                                          "1. Напряжение (в Вольтах, В)\n"
                                          "2. Сопротивление в Омах, Ω)"
                                          "Введите все переменные подряд в формате без запятых. Пример: 2 4")
        user_data[message.chat.id] = {"task": "сила тока в цепи"}


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "давление газа")
def pressure(message):
    message_str = str(message.text)
    message_list = message_str.split()
    try:
        n = float(message_list[0])
        t = float(message_list[1])
        v = float(message_list[2])
        r = 8.314
        answer = (n * r * t) / v
        bot.send_message(message.chat.id, f'Ответом будет {answer}')

    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "средняя скорость молекул")
def molecule_speed(message):
    message_str = str(message.text)
    message_list = message_str.split()
    try:
        t = float(message_list[0])
        m = float(message_list[1])
        k = 1.38e-23
        answer = math.sqrt((3 * k * t) / m)
        bot.send_message(message.chat.id, f'Ответом будет {answer}')
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "работа газа")
def gas_operation(message):
    message_str = str(message.text)
    message_list = message_str.split()
    try:
        p = float(message_list[0])
        delta_v = float(message_list[1])
        answer = p * delta_v
        bot.send_message(message.chat.id, f'Ответом будет {answer}')
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "сила тока в цепи")
def current_in_the_circuit(message):
    message_str = str(message.text)
    message_list = message_str.split()
    try:
        u = float(message_list[0])
        r = float(message_list[1])
        answer = u / r
        bot.send_message(message.chat.id, f'Ответом будет {answer}')
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")




# Запрос данных для расчета скорости
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "скорость")
def get_speed_data(message):
    try:
        s = float(message.text)  # путь
        user_data[message.chat.id]["s"] = s
        bot.send_message(message.chat.id, "Введите время (в секундах):")
        bot.register_next_step_handler(message, calculate_speed)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")

# Расчет скорости
def calculate_speed(message):
    try:
        t = float(message.text)  # время
        s = user_data[message.chat.id]["s"]  # путь
        v = s / t  # Расчет скорости
        bot.send_message(message.chat.id, f"Скорость v = {v} м/с")
        go_to_main_menu(message)  # Возвращаем в главное меню после расчёта
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")

# Запрос данных для расчета времени
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "время")
def get_time_data(message):
    try:
        s = float(message.text)  # путь
        user_data[message.chat.id]["s"] = s
        bot.send_message(message.chat.id, "Введите скорость (в м/с):")
        bot.register_next_step_handler(message, calculate_time)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")

# Расчет времени
def calculate_time(message):
    try:
        v = float(message.text)  # скорость
        s = user_data[message.chat.id]["s"]  # путь
        t = s / v  # Расчет времени
        bot.send_message(message.chat.id, f"Время t = {t} секунд")
        go_to_main_menu(message)  # Возвращаем в главное меню после расчёта
    except ValueError:
         bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")

# Запрос данных для расчета пути
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "путь")
def get_distance_data(message):
    try:
         v = float(message.text)  # скорость
         user_data[message.chat.id]["v"] = v
         bot.send_message(message.chat.id, "Введите время (в секундах):")
         bot.register_next_step_handler(message, calculate_distance)
    except ValueError:
         bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")

# Расчет пути
def calculate_distance(message):
    try:
         t = float(message.text)  # время
         v = user_data[message.chat.id]["v"]  # скорость
         s = v * t  # Расчет пути
         bot.send_message(message.chat.id, f"Путь s = {s} метров")
         go_to_main_menu(message)  # Возвращаем в главное меню после расчёта
    except ValueError:
         bot.send_message(message.chat.id,"Неверный формат данных , попробуйте снова.")

# Запрос данных для расчета ускорения
@bot.message_handler(func=lambda message: user_data.get( message .chat .id , {}).get( 'task') == 'ускорение')
def get_acceleration_data( message ):
     try:
         delta_v=float( message.text )   # изменение скорости
         user_data[message .chat .id]['delta_v']
         bot .send_message( message .chat .id , 'Введите время ( в секундах ):')
         bot.register_next_step_handler( message , calculate_acceleration )
     except ValueError:
         bot .send_message( message .chat .id , 'Неверный формат данных , попробуйте снова.')

# Расчет ускорения
def calculate_acceleration( message ):
     try:
         t=float( message.text )   # время
         delta_v=user_data[message .chat .id]['delta_v']   # изменение скорости
         a=delta_v / t  # Расчет ускорения
         bot .send_message( message .chat .id , f'Ускорение a={a} м/с²')
         go_to_main_menu( message )   # Возвращаем в главное меню после расчёта
     except ValueError:
         bot .send_message( message .chat .id,'Неверный формат данных , попробуйте снова.')

# Запрос данных для расчета импульса
@bot.message_handler(func=lambda message: user_data.get( message .chat .id , {}).get( 'task') == 'импульс')
def get_impulse_data( message ):
     try:
         m=float( message.text )   # масса
         user_data[message .chat .id]['m']
         bot .send_message( message .chat .id , 'Введите скорость ( в м/с ):')
         bot.register_next_step_handler( message , calculate_impulse )
     except ValueError:
         bot .send_message( message .chat .id , 'Неверный формат данных , попробуйте снова.')

# Расчет импульса
def calculate_impulse( message ):
     try:
         v=float( message.text )   # скорость
         m=user_data[message .chat .id]['m']   # масса
         p=m*v   # Расчет импульса
         bot.send_message( message .chat .id , f'Импульс p={p} кг·м/с')
         go_to_main_menu( message )   # Возвращаем в главное меню после расчёта
     except ValueError:
         bot.send_message( message .chat .id , 'Неверный формат данных , попробуйте снова.')

# Функция для возврата в главное меню
def go_to_main_menu( message ):
     markup=types.ReplyKeyboardMarkup(row_width=2)
     item1=types.KeyboardButton('МКТ')
     item2=types.KeyboardButton('Базовые задачи')
     item3=types.KeyboardButton('Термодинамика')
     item4=types.KeyboardButton('Цепи')
     markup.add(item1,item2,item3,item4)
     bot.send_message( message .chat .id ,'Задача решена! Выберите другую категорию:', reply_markup=markup)

if __name__ == '__main__':
    while True:
       try:
           bot.infinity_polling(none_stop=True)
       except Exception as e:
           print(f"Ошибка: {e}")
           time.sleep(5)  # Задержка перед повторной попыткой1
