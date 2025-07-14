import telebot
from telebot import types
import psycopg2
from psycopg2 import sql

API_TOKEN = '***'
bot = telebot.TeleBot(API_TOKEN)

# Параметры подключения к БД
DB_NAME = 'test'
DB_USER = 'vlados'
DB_PASSWORD = 'vlados'
DB_HOST = 'localhost'
DB_PORT = '5432'


# Создаем базу данных
def create_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (name TEXT, age INTEGER, city TEXT, children INTEGER, population INTEGER)''')
    conn.commit()
    cursor.close()
    conn.close()


create_db()

# Словарь для хранения данных о пользователях
user_data = {}

# Список регионов
regions = [
    "Алтайский край",
    "Амурская область",
    "Архангельская область",
    "Астраханская область",
    "Белгородская область",
    "Брянская область",
    "Владимирская область",
    "Волгоградская область",
    "Вологодская область",
    "Воронежская область",
    "г. Москва",
    "г. Севастополь",
    "г.Санкт-Петербург",
    "ДНР",
    "Забайкальский край",
    "Запорожская область",
    "Ивановская область",
    "Иркутская область",
    "Кабардино-Балкарская Республика",
    "Калиниградская область",
    "Калужская область",
    "Камчатский край",
    "Кемеровская область",
    "Кировская область",
    "Костромская область",
    "Краснодарский край",
    "Красноярский край",
    "Курганская область",
    "Курская область",
    "Ленинградская область",
    "Липецкая область",
    "ЛНР",
    "Магаданская область",
    "Московская область",
    "Мурманская область",
    "Нижегородская область",
    "Новгородская область",
    "Новосибирская область",
    "Омская область",
    "Оренбургская область",
    "Орловская область",
    "Пензенская область",
    "Пермский край",
    "Приморский край",
    "Псковская область",
    "Республика Адыгея",
    "Республика Алтай",
    "Республика Башкортостан",
    "Республика Бурятия",
    "Республика Дагестан",
    "Республика Калмыкия",
    "Республика Карелия",
    "Республика Коми",
    "Республика Крым",
    "Республика Марий Эл",
    "Республика Мордовия",
    "Республика Саха (Якутия)",
    "Республика Татарстан",
    "Республика Тыва",
    "Республика Хакасия",
    "Ростовская область",
    "Рязанская область",
    "Самарская область",
    "Саратовская область",
    "Сахалинская область",
    "Свердловская область",
    "Смоленская область",
    "Ставропольский край",
    "Тамбовская область",
    "Тверская область",
    "Томская область",
    "Тульская область",
    "Тюменская область",
    "Удмурсткая Республика",
    "Ульяновская область",
    "Хабаровский край",
    "Ханты-Мансийский АО",
    "Херсонская область",
    "Челябинская область",
    "Чувашская Республика",
    "Ямало-Ненецкий АО",
    "Ярославская область"
]


# Начало диалога
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Начать")
    keyboard.add(start_button)
    # back_button = types.KeyboardButton("Назад")
    # keyboard.add(back_button)

    bot.send_message(message.chat.id,
                     "Приветствуем!\nВпереди Вас ждет несколько вопросов о вскармливании ребенка.\nЭто небольшой вклад в большое дело!\nНажмите «Начать».",
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_name)


# Запрос имени
def ask_name(message):
    if message.text == "Начать":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите ваше имя:", reply_markup=keyboard)
        bot.register_next_step_handler(message, ask_age)
    # elif message.text == "Назад":
    #    bot.send_message(message.chat.id, "Вы вернулись в начало.")
    #    start(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, нажмите 'Начать'.")
        start(message)


# Запрос возраста
def ask_age(message):
    user_id = message.chat.id
    user_data[user_id] = {'name': message.text}

    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Введите ваш возраст:", reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_region)


def ask_region(message):
    user_id = message.chat.id
    user_data[user_id]['age'] = message.text

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for region in regions:
        keyboard.add(types.KeyboardButton(region))
    back_button = types.KeyboardButton("Назад")
    keyboard.add(back_button)

    bot.send_message(message.chat.id, "Выберите ваш регион:", reply_markup=keyboard)
    bot.register_next_step_handler(message, process_region_choice)


def process_region_choice(message):
    user_id = message.chat.id
    if message.text == "Назад":
        ask_age(message)
    else:
        user_data[user_id]['region'] = message.text
        if message.text in ["г. Москва", "г. Севастополь", "г.Санкт-Петербург"]:
            ask_children(message)
        else:
            ask_population(message)


def ask_population(message):
    user_id = message.chat.id
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Введите количество населения в вашем городе:", reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_children)


def ask_children(message):
    user_id = message.chat.id
    if 'population' not in user_data[user_id]:
        user_data[user_id]['population'] = message.text

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton("Да")
    no_button = types.KeyboardButton("Нет")
    back_button = types.KeyboardButton("Назад")
    keyboard.add(yes_button, no_button, back_button)

    bot.send_message(message.chat.id, "У вас есть дети?", reply_markup=keyboard)
    bot.register_next_step_handler(message, process_children_choice)


def process_children_choice(message):
    user_id = message.chat.id
    if message.text.lower() == 'да':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите количество детей:", reply_markup=keyboard)
        bot.register_next_step_handler(message, confirm_data)
    elif message.text.lower() == "нет":
        user_data[user_id]['children'] = 0
        confirm_data(message)
    elif message.text == "Назад":
        if user_data[user_id]['region'] in ["г. Москва", "г. Севастополь", "г.Санкт-Петербург"]:
            ask_region(message)
        else:
            ask_population(message)


def confirm_data(message):
    user_id = message.chat.id
    if 'children' not in user_data[user_id]:
        user_data[user_id]['children'] = message.text

    name = user_data[user_id]['name']
    age = user_data[user_id]['age']
    region = user_data[user_id]['region']
    children = user_data[user_id]['children']
    population = user_data.get('population', 'Не указано')

    confirmation_text = f"Подтвердите ваши данные:\nИмя: {name}\nВозраст: {age}\nРегион: {region}\nНаселение: {population}\nДети: {children}"

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.KeyboardButton("Подтвердить")
    edit_button = types.KeyboardButton("Редактировать")
    back_button = types.KeyboardButton("Назад")
    keyboard.add(confirm_button, edit_button, back_button)

    bot.send_message(message.chat.id, confirmation_text, reply_markup=keyboard)


# Обработка подтверждения
@bot.message_handler(content_types=['text'])
def confirm_callback(message):
    if message.text == "Подтвердить":
        user_id = message.chat.id
        name = user_data[user_id]['name']
        age = user_data[user_id]['age']
        region = user_data[user_id]['region']
        children = user_data[user_id]['children']
        population = user_data.get('population', 0)

        save_data(name, age, region, children, population)

        bot.send_message(message.chat.id, "Данные успешно подтверждены и сохранены!")

    elif message.text == "Редактировать":
        show_edit_options(message)

    elif message.text == "Назад":
        ask_children(message)


# Функция для показа опций редактирования
def show_edit_options(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    name_button = types.KeyboardButton("Имя")
    age_button = types.KeyboardButton("Возраст")
    region_button = types.KeyboardButton("Регион")
    children_button = types.KeyboardButton("Дети")
    population_button = types.KeyboardButton("Население")
    keyboard.add(name_button, age_button, region_button, children_button, population_button)
    back_button = types.KeyboardButton("Назад")
    keyboard.add(back_button)

    bot.send_message(message.chat.id, "Выберите поле для редактирования:", reply_markup=keyboard)
    bot.register_next_step_handler(message, edit_data)


# Обработка редактирования
def edit_data(message):
    user_id = message.chat.id
    if message.text == "Имя":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите новое имя:", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda m: edit_name(m))
    elif message.text == "Возраст":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите новый возраст:", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda m: edit_age(m))
    elif message.text == "Регион":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for region in regions:
            keyboard.add(types.KeyboardButton(region))
        back_button = types.KeyboardButton("Назад")
        keyboard.add(back_button)

        bot.send_message(message.chat.id, "Выберите новый регион:", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda m: edit_region(m))
    elif message.text == "Дети":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите новое количество детей:", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda m: edit_children(m))
    elif message.text == "Население":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите новое количество населения:", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda m: edit_population(m))
    elif message.text == "Назад":
        confirm_data(message)


def edit_name(message):
    user_id = message.chat.id
    user_data[user_id]['name'] = message.text
    confirm_data(message)


def edit_age(message):
    user_id = message.chat.id
    user_data[user_id]['age'] = message.text
    confirm_data(message)


def edit_region(message):
    user_id = message.chat.id
    user_data[user_id]['region'] = message.text
    if message.text in ["г. Москва", "г. Севастополь", "г.Санкт-Петербург"]:
        ask_children(message)
    else:
        ask_population(message)


def edit_children(message):
    user_id = message.chat.id
    user_data[user_id]['children'] = message.text
    confirm_data(message)


def edit_population(message):
    user_id = message.chat.id
    user_data[user_id]['population'] = message.text
    confirm_data(message)


# Сохранение данных в БД
def save_data(name, age, region, children, population):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, age, city, children, population) VALUES (%s, %s, %s, %s, %s)",
                       (name, int(age), region, int(children), int(population)))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
    finally:
        cursor.close()
        conn.close()


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
