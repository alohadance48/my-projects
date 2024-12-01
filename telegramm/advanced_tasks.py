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

@bot.message_handler(func=lambda message: message.text == "МКТ")
def mkt_category(message):
    bot.send_message(message.chat.id, "Ты выбрал категорию: МКТ. Напиши задачу.")
    user_data[message.chat.id] = {"category": "МКТ"}

@bot.message_handler(func=lambda message: message.text == "Термодинамика")
def thermodynamics_category(message):
    bot.send_message(message.chat.id, "Ты выбрал категорию: Термодинамика. Напиши задачу.")
    user_data[message.chat.id] = {"category": "Термодинамика"}

@bot.message_handler(func=lambda message: message.text == "Цепи")
def chains_category(message):
    bot.send_message(message.chat.id, "Ты выбрал категорию: Цепи. Напиши задачу.")
    user_data[message.chat.id] = {"category": "Цепи"}

# Примерные решения задач для МКТ, термодинамики и цепей

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "МКТ")
def mkt_task(message):
    bot.send_message(message.chat.id, "Пример задачи МКТ:\n"
                                      "В идеальном газе объем 5 м³ при температуре 300 К. "
                                      "Найдите давление газа при известной постоянной Р."
                                      " P = n * R * T / V")
    user_data[message.chat.id]["task"] = "mkt"

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "Термодинамика")
def thermodynamics_task(message):
    bot.send_message(message.chat.id, "Пример задачи по термодинамике:\n"
                                      "Найдите работу газа при адиабатическом процессе.")
    user_data[message.chat.id]["task"] = "thermo"

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "Цепи")
def chains_task(message):
    bot.send_message(message.chat.id, "Пример задачи по цепям:\n"
                                      "Решение задачи на закон Ома для замкнутого контура.")
    user_data[message.chat.id]["task"] = "chains"

bot.polling()
