import telebot
from telebot import types
import datetime
import random
import time  # Import the time module

BOT_TOKEN = "***"
bot = telebot.TeleBot(BOT_TOKEN)

tasks = {}
finances = {}
promotions = {}
events = {}

business_advice = [
    "Фокусируйтесь на потребностях клиентов.",
    "Не бойтесь экспериментировать и адаптироваться.",
    "Инвестируйте в маркетинг и развитие бренда.",
    "Автоматизируйте рутинные задачи.",
    "Следите за конкурентами, но не копируйте их.",
    "Постоянно обучайтесь и развивайте свои навыки.",
    "Делегируйте задачи, чтобы освободить время для стратегии."
]

def get_user_id(message):
    return message.from_user.id

def get_tasks(user_id):
    return tasks.get(user_id, [])

def get_finance_data(user_id):
    return finances.get(user_id, [])

def get_finance_summary(user_id):
    income = sum(item[3] for item in get_finance_data(user_id) if item[1] == "income")
    expense = sum(item[3] for item in get_finance_data(user_id) if item[1] == "expense")
    return income, expense

def get_promotions(user_id):
    return promotions.get(user_id, [])

def get_events(user_id):
    return events.get(user_id, {})

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавить задачу")
    item2 = types.KeyboardButton("Просмотреть задачи")
    item3 = types.KeyboardButton("Удалить задачу")
    item4 = types.KeyboardButton("Добавить доход")
    item5 = types.KeyboardButton("Добавить расход")
    item6 = types.KeyboardButton("Финансовый отчет")
    item7 = types.KeyboardButton("Бизнес-совет")
    item8 = types.KeyboardButton("Управление акциями")
    item9 = types.KeyboardButton("Анализ рынка")
    item10 = types.KeyboardButton("Календарь событий")
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
    bot.reply_to(message, "Привет! Я бот для малого бизнеса. Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Добавить задачу")
def add_task_handler(message):
    bot.reply_to(message, "Ок, опишите задачу и укажите срок (например: Купить канцтовары - 2024-02-15)")
    bot.register_next_step_handler(message, process_add_task)

def process_add_task(message):
    try:
        task_description, due_date_str = message.text.split(" - ")
        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
        user_id = get_user_id(message)
        if user_id not in tasks:
            tasks[user_id] = []
        tasks[user_id].append((task_description, due_date.strftime("%Y-%m-%d")))
        bot.reply_to(message, f"Задача '{task_description}' добавлена на {due_date.strftime('%Y-%m-%d')}")
    except Exception as e:
        bot.reply_to(message, "Неверный формат. Пожалуйста, опишите задачу и укажите срок (например: Купить канцтовары - 2024-02-15)")

@bot.message_handler(func=lambda message: message.text == "Просмотреть задачи")
def view_tasks_handler(message):
    user_id = get_user_id(message)
    user_tasks = get_tasks(user_id)
    if user_tasks:
        task_list = "\n".join([f"- {task[0]} (до {task[1]})" for task in user_tasks])
        bot.reply_to(message, f"Ваши задачи:\n{task_list}")
    else:
        bot.reply_to(message, "Нет активных задач.")

@bot.message_handler(func=lambda message: message.text == "Удалить задачу")
def delete_task_handler(message):
    user_id = get_user_id(message)
    user_tasks = get_tasks(user_id)
    if not user_tasks:
        bot.reply_to(message, "Нет задач для удаления.")
        return

    markup = types.InlineKeyboardMarkup()
    for i, task in enumerate(user_tasks):
        markup.add(types.InlineKeyboardButton(text=f"Удалить: {task[0]}", callback_data=f"delete_task_{user_id}_{i}"))

    bot.send_message(message.chat.id, "Выберите задачу для удаления:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_task_"))
def process_delete_task_callback(call):
    _, user_id, task_index = call.data.split("_")
    user_id = int(user_id)
    task_index = int(task_index)

    user_tasks = get_tasks(user_id)
    if user_tasks and 0 <= task_index < len(user_tasks):
        deleted_task = user_tasks.pop(task_index)
        tasks[user_id] = user_tasks
        bot.answer_callback_query(call.id, text=f"Задача '{deleted_task[0]}' удалена.")
        bot.send_message(call.message.chat.id, f"Задача '{deleted_task[0]}' удалена.")
    else:
        bot.answer_callback_query(call.id, text="Задача не найдена.")
        bot.send_message(call.message.chat.id, "Задача не найдена.")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda message: message.text == "Добавить доход")
def add_income_handler(message):
    bot.reply_to(message, "Введите сумму дохода и описание (например: 15000 - Продажа товара)")
    bot.register_next_step_handler(message, process_add_income)

def process_add_income(message):
    try:
        amount, description = message.text.split(" - ")
        amount = float(amount)
        user_id = get_user_id(message)
        if user_id not in finances:
            finances[user_id] = []
        finances[user_id].append((datetime.date.today().strftime("%Y-%m-%d"), "income", "Other", amount, description))
        bot.reply_to(message, f"Доход {amount} добавлен.")
    except Exception as e:
        bot.reply_to(message, "Неверный формат. Введите сумму и описание (например: 15000 - Продажа товара)")

@bot.message_handler(func=lambda message: message.text == "Добавить расход")
def add_expense_handler(message):
    bot.reply_to(message, "Введите сумму расхода и описание (например: 5000 - Аренда офиса)")
    bot.register_next_step_handler(message, process_add_expense)

def process_add_expense(message):
    try:
        amount, description = message.text.split(" - ")
        amount = float(amount)
        user_id = get_user_id(message)
        if user_id not in finances:
            finances[user_id] = []
        finances[user_id].append((datetime.date.today().strftime("%Y-%m-%d"), "expense", "Other", amount, description))
        bot.reply_to(message, f"Расход {amount} добавлен.")
    except Exception as e:
        bot.reply_to(message, "Неверный формат. Введите сумму и описание (например: 5000 - Аренда офиса)")

@bot.message_handler(func=lambda message: message.text == "Финансовый отчет")
def financial_report_handler(message):
    user_id = get_user_id(message)
    income, expense = get_finance_summary(user_id)
    balance = income - expense
    report = f"Доходы: {income}\nРасходы: {expense}\nБаланс: {balance}"
    bot.reply_to(message, report)

@bot.message_handler(func=lambda message: message.text == "Бизнес-совет")
def business_advice_handler(message):
    advice = random.choice(business_advice)
    bot.reply_to(message, advice)

@bot.message_handler(func=lambda message: message.text == "Управление акциями")
def manage_promotions_handler(message):
    user_id = get_user_id(message)
    bot.reply_to(message, "Введите название акции, описание, дату начала и дату окончания (Например: Летняя распродажа - Скидки до 50% - 2024-06-01 - 2024-08-31)")
    bot.register_next_step_handler(message, process_add_promotion, user_id=user_id)

def process_add_promotion(message, user_id):
    try:
        name, description, start_date_str, end_date_str = message.text.split(" - ")
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

        if user_id not in promotions:
            promotions[user_id] = []
        promotions[user_id].append((name, description, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
        bot.reply_to(message, f"Акция '{name}' добавлена.")

    except Exception as e:
        bot.reply_to(message, "Неверный формат. Введите название акции, описание, дату начала и дату окончания (Например: Летняя распродажа - Скидки до 50% - 2024-06-01 - 2024-08-31)")

@bot.message_handler(func=lambda message: message.text == "Анализ рынка")
def market_analysis_handler(message):
    bot.reply_to(message, "Анализ рынка показывает, что сейчас хорошее время для расширения ассортимента и привлечения новых клиентов.  Не забудьте оценить конкурентов!")

@bot.message_handler(func=lambda message: message.text == "Календарь событий")
def event_calendar_handler(message):
    user_id = get_user_id(message)
    now = datetime.datetime.now()
    calendar = ""
    for i in range(7):
        date = now + datetime.timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        event_list = events.get(user_id, {}).get(date_str, [])
        event_str = ", ".join(event_list) if event_list else "Нет событий"
        calendar += f"{date_str}: {event_str}\n"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавить событие")
    item2 = types.KeyboardButton("Назад")
    markup.add(item1, item2)
    bot.reply_to(message, "Ваш календарь событий на ближайшую неделю:\n" + calendar, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Добавить событие")
def add_event_handler(message):
    bot.reply_to(message, "Введите дату события и описание (например: 2024-02-15 - Встреча с клиентом)")
    bot.register_next_step_handler(message, process_add_event)

def process_add_event(message):
    try:
        date_str, description = message.text.split(" - ")
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        user_id = get_user_id(message)
        date_str = date.strftime("%Y-%m-%d")

        if user_id not in events:
            events[user_id] = {}
        if date_str not in events[user_id]:
            events[user_id][date_str] = []

        events[user_id][date_str].append(description)
        bot.reply_to(message, f"Событие '{description}' добавлено на {date_str}")

    except Exception as e:
        bot.reply_to(message, "Неверный формат. Введите дату события и описание (например: 2024-02-15 - Встреча с клиентом)")

@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_menu(message):
    send_welcome(message)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я не понимаю эту команду.")

# Main loop with error handling
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(15)  # Wait for 15 seconds before restarting
