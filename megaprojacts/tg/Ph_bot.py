import telebot
from sympy import symbols, Eq, solve

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота, полученный от BotFather
TOKEN = '7576640329:AAE5aLRnF_nPcT-qzsGpZ9b2aE7OIAdEO8Y'
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для решения простых задач по физике.\n"
        "Напиши мне задачу в формате:\n"
        "1. Найди силу при массе 10 кг и ускорении 2 м/с².\n"
        "2. Найди работу при силе 5 Н и расстоянии 10 м.\n"
        "3. Найди силу трения при коэффициенте трения 0.5 и нормальной силе 20 Н.\n"
        "4. Найди импульс при массе 10 кг и скорости 3 м/с.\n"
        "5. Найди кинетическую энергию при массе 5 кг и скорости 4 м/с.\n"
        "6. Найди потенциальную энергию при массе 10 кг, высоте 5 м и ускорении свободного падения 9.81 м/с².\n"
        "7. Найди скорость при расстоянии 100 м и времени 10 с."
    )

# Обработчик текста для решения задач по физике
@bot.message_handler(func=lambda message: True)
def solve_physics_task(message):
    text = message.text.lower()

    # Задача: Вычисление силы по формуле F = m * a
    if "силу" in text and "массе" in text and "ускорении" in text:
        try:
            m = float(text.split("массе")[1].split()[0])
            a = float(text.split("ускорении")[1].split()[0])
            F = m * a
            bot.send_message(message.chat.id, f"Сила F = m * a = {m} * {a} = {F} Н")
        except Exception:
            bot.send_message(message.chat.id, "Не удалось распознать значения массы или ускорения.")

    # Задача: Вычисление работы по формуле W = F * d
    elif "работу" in text and "силе" in text and "расстоянии" in text:
        try:
            F = float(text.split("силе")[1].split()[0])
            d = float(text.split("расстоянии")[1].split()[0])
            W = F * d
            bot.send_message(message.chat.id, f"Работа W = F * d = {F} * {d} = {W} Дж")
        except Exception:
            bot.send_message(message.chat.id, "Не удалось распознать значения силы или расстояния.")

    # Задача: Вычисление силы трения по формуле F_t = μ * N
    elif "силу трения" in text and "коэффициенте трения" in text and "нормальной силе" in text:
        try:
            mu = float(text.split("коэффициенте трения")[1].split()[0])
            N = float(text.split("нормальной силе")[1].split()[0])
            F_t = mu * N
            bot.send_message(message.chat.id, f"Сила трения F_t = μ * N = {mu} * {N} = {F_t} Н")
        except Exception:
            bot.send_message(message.chat.id, "Не удалось распознать значения коэффициента трения или нормальной силы.")

    # Задача: Вычисление импульса по формуле p = m * v
    elif "импульс" in text and "массе" in text and "скорости" in text:
        try:
            m = float(text.split("массе")[1].split()[0])
            v = float(text.split("скорости")[1].split()[0])
            p = m * v
            bot.send_message(message.chat.id, f"Импульс p = m * v = {m} * {v} = {p} кг·м/с")
        except Exception:
            bot.send_message(message.chat.id, "Не удалось распознать значения массы или скорости.")

    # Задача: Вычисление кинетической энергии по формуле E_k = (1/2) * m * v^2
    elif "кинетическую энергию" in text and "массе" in text and "скорости" in text:
        try:
            m = float(text.split("массе")[1].split()[0])
            v = float(text.split("скорости")[1].split()[0])
            E_k = 0.5 * m * v ** 2
            bot.send_message(message.chat.id, f"Кинетическая энергия E_k = (1/2) * m * v^2 = (1/2) * {m} * {v}^2 = {E_k} Дж")
        except Exception:
            bot.send_message(message.chat.id, "Не удалось распознать значения массы или скорости.")

    # Задача: Вычисление потенциальной энергии по формуле E_p = mgh
    elif "потенциальную энергию" in text and "массе" in text and "высоте" in text:
        try:
            m = float(text.split("массе")[1].split()[0])
            g = float(text.split("ускорении свободного падения")[1].split()[0]) if 'ускорении свободного падения' in text else 9.81
            h = float(text.split("высоте")[1].split()[0])
            E_p = m * g * h
            bot.send_message(message.chat.id, f"Потенциальная энергия E_p = mgh = {m} * {g} * {h} = {E_p} Дж")
        except Exception:
            bot.send_message(message.chat.id, "Не удалось распознать значения массы, высоты или ускорения свободного падения.")

    # Задача: Вычисление скорости по формуле v = s / t
    elif "скорость" in text and "расстоянии" in text and "времени" in text:
        try:
            s = float(text.split("расстоянии")[1].split()[0])
            t = float(text.split("времени")[1].split()[0])
            v = s / t
            bot.send_message(message.chat.id, f"Скорость v = s / t = {s} / {t} = {v} м/с")
        except Exception:
            bot.send_message(message.chat.id, "Не удалось распознать значения расстояния или времени.")

    # Если задача не распознана
    else:
        bot.send_message(message.chat.id,
                         "Не удалось распознать задачу. Пожалуйста, используйте форматы, указанные в описании.")

# Запуск бота
bot.polling()