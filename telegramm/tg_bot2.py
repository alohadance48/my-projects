import telebot
from telebot import types
import random

# Замените на ваш токен
TELEGRAM_TOKEN = '7893306656:AAHEF6cwBhaPPr7yiURQGcYtMeYJ7aBsJTI'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Хранение задач и финансов (временное хранилище)
tasks = []
finances = []


# Начальная команда
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Добавить задачу"))
    keyboard.add(types.KeyboardButton("Список задач"))
    keyboard.add(types.KeyboardButton("Добавить доход"))
    keyboard.add(types.KeyboardButton("Добавить расход"))
    keyboard.add(types.KeyboardButton("Показать баланс"))
    keyboard.add(types.KeyboardButton("Получить бизнес-совет"))

    bot.send_message(message.chat.id, "Привет! Я бот для предпринимателей. Выберите действие:", reply_markup=keyboard)


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Добавить задачу":
        bot.send_message(message.chat.id, "Введите задачу:")
        bot.register_next_step_handler(message, add_task)
    elif message.text == "Список задач":
        list_tasks(message)
    elif message.text == "Добавить доход":
        bot.send_message(message.chat.id, "Введите сумму дохода:")
        bot.register_next_step_handler(message, add_income)
    elif message.text == "Добавить расход":
        bot.send_message(message.chat.id, "Введите сумму расхода:")
        bot.register_next_step_handler(message, add_expense)
    elif message.text == "Показать баланс":
        show_balance(message)
    elif message.text == "Получить бизнес-совет":
        give_advice(message)


def add_task(message):
    task = message.text
    tasks.append(task)
    bot.send_message(message.chat.id, f'Задача добавлена: {task}')


def list_tasks(message):
    if tasks:
        tasks_list = '\n'.join([f"{i + 1}. {task}" for i, task in enumerate(tasks)])
        bot.send_message(message.chat.id, f'Ваши задачи:\n{tasks_list}')
    else:
        bot.send_message(message.chat.id, 'Задачи отсутствуют.')


def add_income(message):
    try:
        income = float(message.text)
        finances.append(income)
        bot.send_message(message.chat.id, f'Добавлен доход: {income}')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите корректную сумму дохода.')


def add_expense(message):
    try:
        expense = float(message.text)
        finances.append(-expense)
        bot.send_message(message.chat.id, f'Добавлен расход: {expense}')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите корректную сумму расхода.')


def show_balance(message):
    total_balance = sum(finances)
    bot.send_message(message.chat.id, f'Ваш текущий баланс: {total_balance}')


def give_advice(message):
    business_advice = [
        "Не бойтесь рисковать.",
        "Слушайте своих клиентов.",
        "Инвестируйте в маркетинг.",
        "Не забывайте о своих конкурентах.",
        "Ставьте реалистичные цели."
        "Отсосать начальнику"
    ]

    advice = random.choice(business_advice)
    bot.send_message(message.chat.id, f'Совет: {advice}')


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
