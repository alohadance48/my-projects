import telebot
from telebot import types

TOKEN = 'your_token'  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message)

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton("МКТ")
    item2 = types.KeyboardButton("Базовые задачи")
    item3 = types.KeyboardButton("Термодинамика")
    item4 = types.KeyboardButton("Цепи")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Привет! Выберите категорию для решения задачи:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Базовые задачи")
def select_basic_task(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton("Скорость")
    item2 = types.KeyboardButton("Время")
    item3 = types.KeyboardButton("Путь")
    item4 = types.KeyboardButton("Ускорение")
    item5 = types.KeyboardButton("Импульс")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, "Выбери задачу, которую хочешь решить:", reply_markup=markup)
    user_data[message.chat.id] = {"category": "Базовые задачи"}

@bot.message_handler(func=lambda message: message.text in ["Скорость", "Время", "Путь", "Ускорение", "Импульс"])
def ask_for_data(message):
    task = message.text
    if task == "Скорость":
        bot.send_message(message.chat.id, "Для расчета скорости мне нужны следующие данные:\n"
                                            "1. Путь (в метрах)\n"
                                            "2. Время (в секундах)\n"
                                            "Введите путь:")
        user_data[message.chat.id] = {"task": "скорость"}
    elif task == "Время":
        bot.send_message(message.chat.id, "Для расчета времени мне нужны следующие данные:\n"
                                            "1. Путь (в метрах)\n"
                                            "2. Скорость (в м/с)\n"
                                            "Введите путь:")
        user_data[message.chat.id] = {"task": "время"}
    elif task == "Путь":
        bot.send_message(message.chat.id, "Для расчета пути мне нужны следующие данные:\n"
                                            "1. Скорость (в м/с)\n"
                                            "2. Время (в секундах)\n"
                                            "Введите скорость:")
        user_data[message.chat.id] = {"task": "путь"}
    elif task == "Ускорение":
        bot.send_message(message.chat.id, "Для расчета ускорения мне нужны следующие данные:\n"
                                            "1. Начальная скорость (в м/с)\n"
                                            "2. Конечная скорость (в м/с)\n"
                                            "3. Время (в секундах)\n"
                                            "Введите начальную скорость:")
        user_data[message.chat.id] = {"task": "ускорение"}
    elif task == "Импульс":
        bot.send_message(message.chat.id, "Для расчета импульса мне нужны следующие данные:\n"
                                            "1. Масса (в килограммах)\n"
                                            "2. Скорость (в м/с)\n"
                                            "Введите массу:")
        user_data[message.chat.id] = {"task": "импульс"}

# Расчёты и запрос данных для задач (скорость, время, путь и т.д.) оставляем без изменений.

bot.polling()
