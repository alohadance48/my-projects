import telebot
from telebot import types
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import logging
import threading
import concurrent.futures
import time

# Настройка логирования
logging.basicConfig(level=logging.ERROR, filename="bot.log", filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')
user_locks = {}  # Словарь для блокировок пользователей

# Токен вашего бота (лучше хранить в переменной окружения)
TOKEN = '***'
if not TOKEN:
    print("Ошибка: Не найден токен бота в переменных окружения.")
    exit()
# Создаем словарь с путями к изображениям для каждого отдела
department_images = {
    'И': '/home/vlados/photos_for_bot/event.jpg',
    'dept2': '/path/to/image2.png',
    # Добавьте здесь пути к изображениям для всех отделов
}

# Теперь вы можете использовать этот словарь в функции send_department_result

bot = telebot.TeleBot(TOKEN, threaded=True)

# Путь к файлу с ключами для Google Sheets API (лучше хранить в переменной окружения)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'key.json'
if not SERVICE_ACCOUNT_FILE:
    print("Ошибка: Не найден путь к файлу credentials.json в переменных окружения.")
    exit()

# ID таблицы Google Sheets
SPREADSHEET_ID = '***'
if not SPREADSHEET_ID:
    print("Ошибка: Не найден ID Google Sheet в переменных окружения.")
    exit()

image_folder = '/home/vladosl/photos_for_bot'

# Диапазон для записи данных
RANGE_NAME = 'Лист1!A1'

# Создание сервисного аккаунта
try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Создание клиента Google Sheets API
    service = build('sheets', 'v4', credentials=credentials)
    print(credentials.service_account_email)

except Exception as e:
    logging.error(f"Ошибка при создании сервисного аккаунта: {e}")
    print(f"Ошибка при создании сервисного аккаунта: {e}")
    exit()

# Словарь для хранения ответов пользователя
user_answers = {}

# Словарь для подсчета упоминаний отделов
departments = {}

user_locks = {}  # Словарь для блокировок пользователей
user_steps = {}  # Словарь для отслеживания шагов пользователя
selected_departments = {}  # Словарь для выбранных отделов
user_department_sent = {}
apply_button_images = {
    'М': 'apply_methodic.jpg',
    'HR': 'apply_hr.jpg',
    'И': 'apply_event.jpg',
    'Н': 'apply_nabor.jpg',
    'П': 'apply_partner.jpg',
    'А': 'apply_admin.jpg'
}
# Словарь с вопросами и вариантами ответов
questions = {
    1: {
        'question': '*Вы - организатор мастер-класса «Я в деле». Чем займетесь?*',
        'options': {
            'А': 'Подберу площадку, позабочусь о техническом оборудовании',
            'Б': 'Сделаю так, чтобы пришло много участников',
            'В': 'Продумаю план выступления, подготовлю презентацию',
            'Г': 'Подберу эксперта, соберу обратную связь',
            'Д': 'Возьму на себя отчетность',
            'Е': 'Налажу контакт с представителями вуза, подумаю, чем они могут быть полезны'
        }
    },
    2: {
        'question': '*Выберите утверждения, которые вас описывают*',
        'options': {
            'А': 'Я умею вдохновлять людей идеей',
            'Б': 'Я люблю работать с командами и их развитием',
            'В': 'Я – крутой организатор',
            'Г': 'Я легко выхожу на контакт с людьми',
            'Д': 'Я хорошо работаю с таблицами, внимательный',
            'Е': 'Я креативный человек, люблю создавать что-то новое'
        }
    },
    3: {
        'question': '*Какой подарок вы бы точно оценили?*',
        'options': {
            'А': 'Сертификат на образовательный курс',
            'Б': 'Знакомство с владельцем крупной компании',
            'В': 'Сессия с психологом/ментором',
            'Г': 'Коробка с канцелярией',
            'Д': 'Поездка на июльку',
            'Е': 'Укомплектованная структура'
        }
    },
    4: {
        'question': '*Какое высказывание лучше отражает вашу жизненную позицию?*',
        'options': {
            'А': 'Дьявол в мелочах',
            'Б': 'Чем больше - тем лучше!',
            'В': 'Планирование - это ключ к действию',
            'Г': 'Сила - это люди',
            'Д': 'Если это не зафиксировано - это не существует',
            'Е': 'Никогда не знаешь, кто и когда окажется для тебя полезным'
        }
    },
    5: {
        'question': '*Какая картинка вам больше всего нравится?*',
        'options': {
            'А': 'Картинка 1',
            'Б': 'Картинка 2',
            'В': 'Картинка 3',
            'Г': 'Картинка 4',
            'Д': 'Картинка 5',
            'Е': 'Картинка 6'
        }
    },
    'position': {
        'question': '*Какая у тебя должность?*',
        'options': {
            'Младший наставник': 'Младший наставник',
            'Старший наставник': 'Старший наставник',
            'Координатор': 'Координатор'
        }
    },
    'department': {
        'question': '*Какой отдел тебе интересен?*',
        'options': {
            'М': 'Методический отдел',
            'HR': 'HR-отдел',
            'И': 'Event-отдел',
            'Н': 'Наборный штаб',
            'П': 'Партнерский отдел',
            'А': 'Административный отдел'
        }
    }
}

# Словарь с описаниями отделов и картинками
department_descriptions = {
    'М': {
        'name': '🤔Алеша распределяет тебя в...',
        'description': """
*Методический отдел*

_Подсчет рейтинга команд? Новый предпринимательский курс? Организация образовательных мероприятий?_ 

Теперь это может стать не разрывно связанными с тобой вещами, ведь *ты – кандидат в методический отдел.* 

У тебя хорошие аналитические способности: ты сможешь эффективно разрабатывать и оценивать образовательные программы. 

📩 Ты достаточно организованный, а это поможет планировать и координировать все то, что придумал с командой!

*Поздравляем!!!*🥳""",
        'image': 'methodic.jpg'
    },
    'HR': {
        'name': '🤔Алеша распределяет тебя в...',
        'description': """*HR отдел*

_Корпоративы, обучения команды, социология, разработка новых инструментов работы со структурой в 600 человек._ 

И это не мечта, а реальность:
*отдел по развитию талантов и внедрению инноваций [HR].*

📩 Ты показал себя командным и вдохновляющим человеком, поэтому лучше тебя никто не придумает программу внутренних соревнований на сезон!

Ты по-настоящему ценишь людей в своем окружении и стремишься к тому, чтобы рядом с тобой развивались.

Теперь ты на шаг ближе к реализации своих идей внутри Программы.

*Поздравляем!!!*🥳""",
        'image': 'IMG_1862.JPG'
    },
    'И': {
        'name': '🤔Алеша распределяет тебя в...',
        'description': """*Event отдел*

_Открытие? Битва проектов? Закупка и печатка всего-всего-всего? Июлька?_

Да, друг!
*Ты – тот еще организатор!*

📩 Твои организаторские способности, умение держать в голове много задач, творческий подход и навык работы в команде – на высочайшем уровне.

А если хочешь развивать их сильнее, то Алеша рекомендует прислушаться)

Ведь именно ты можешь стать частью самых масштабных проектов Программы!

*Поздравляем!!!*🥳""",
        'image': 'event.jpg'
    },
    'Н': {
        'name': '🤔Алеша распределяет тебя в...',
        'description': """*Наборный отдел*

_План на захват всех вузов и набор участников: есть._
_Ты в этом плане: теперь тоже!_

📩 У тебя *отличные коммуникативные способности*, что позволяет тебе договариваться о проведении любых мероприятий для студентов.

А самое главное – ты умеешь вдохновлять других людей своей идеей и строить отношения вдолгую. 

_Так не каждый сможет!_ 
В команде точно найдешь единомышленников.

*Поздравляем!!!*🥳""",
        'image': 'nabor.jpg'
    },
    'П': {
        'name': '🤔Алеша распределяет тебя в...',
        'description': """*Партнерский отдел*... _Так сразу и подумали, что это про тебя. Деловой успех виден сразу!_... 📩  У тебя блистательные *навыки переговоров* – ты точно сможешь достичь взаимовыгодных соглашений. 

Ты *мыслишь стратегически* – видишь, кто может быть полезен для Программы, умеешь строить долгосрочные связи. Перспективно!

*Поздравляем!!!*🥳""",
        'image': 'partner.jpg'
    },
    'А': {
        'name': '🤔Алеша распределяет тебя в...',
        'description': """*Наборный отдел*

_План на захват всех вузов и набор участников: есть._
_Ты в этом плане: теперь тоже!_

📩 *У тебя отличные коммуникативные способности,* что позволяет тебе договариваться о проведении любых мероприятий для студентов.

А самое главное – ты умеешь вдохновлять других людей своей идеей и строить отношения вдолгую. 

_Так не каждый сможет!_ 
В команде точно найдешь единомышленников.

*Поздравляем!!!*🥳""",
        'image': 'admin.jpg'
    }
}

# Словарь для перевода вариантов ответов пользователя в отделы
answer_to_department = {
    'А': 'И',
    'Б': 'Н',
    'В': 'М',
    'Г': 'HR',
    'Д': 'А',
    'Е': 'П'
}
# Словарь для перевода букв в отделы для последнего вопроса
answer_to_department_last = {
    'А': 'HR',
    'Б': 'П',
    'В': 'А',
    'Г': 'Н',
    'Д': 'М',
    'Е': 'И'
}

# Словарь с изображениями для последнего вопроса
images = {
    'А': 'IMG_1862.jpg',
    'Б': 'partner.jpg',
    'В': 'admin.jpg',
    'Г': 'nabor.jpg',
    'Д': 'methodic.jpg',
    'Е': 'event.jpg'
}

# Функция для создания inline-клавиатуры
user_steps = {}


def send_question(chat_id, question_number):
    if question_number == 5:
        media = []
        image_found = True  # Флаг, указывающий, были ли найдены все изображения
        opened_files = []  # Список для хранения открытых файлов

        for option in ['А', 'Б', 'В', 'Г', 'Д', 'Е']:
            image_path = os.path.join(image_folder, f"{images[option]}")
            try:
                image_file = open(image_path, 'rb')  # Открываем файл
                opened_files.append(image_file)  # Добавляем файл в список
                media.append(types.InputMediaPhoto(media=image_file, caption=f'Вариант {option}'))
            except FileNotFoundError:
                logging.error(f"Image file not found: {image_path}")
                bot.send_message(chat_id, f"Изображение для варианта {option} не найдено.")
                image_found = False  # Устанавливаем флаг в False
                break  # Прерываем цикл, если хотя бы одно изображение не найдено
            except Exception as e:
                logging.error(f"Error reading image file: {image_path} - {e}")
                bot.send_message(chat_id, f"Ошибка чтения изображения для варианта {option}.")
                image_found = False  # Устанавливаем флаг в False
                break  # Прерываем цикл при любой другой ошибке чтения

        if image_found and media:  # Отправляем изображения только если все файлы найдены
            try:
                send_media_group_with_retries(chat_id, media)
            except Exception as e:
                logging.error(f"Unexpected error sending media group: {e}")
                bot.send_message(chat_id, "Неожиданная ошибка при отправке изображений.")
            finally:
                # Закрываем все открытые файлы после отправки
                for file in opened_files:
                    file.close()
        elif not image_found:
            bot.send_message(chat_id, "Не удалось отправить изображения, так как не все файлы найдены.")

    # Отправка вопросов после изображений
    question_text = f"**Вопрос {question_number}:**\n{questions[question_number]['question']}\n\n"
    options_text = "\n".join(
        [f"{option}: {description}" for option, description in questions[question_number]['options'].items()]
    )

    bot.send_message(chat_id, f"{question_text}\n{options_text}", parse_mode="Markdown")

    # Задержка 5 секунд между первым и вторым вопросом, 3 секунды для остальных
    if question_number == 1:
        time.sleep(5)
    else:
        time.sleep(3)

    bot.send_message(chat_id, "Выберите ответ:", reply_markup=create_markup(question_number))


def send_media_group_with_retries(chat_id, media, retries=3, delay=5):
    for attempt in range(retries):
        try:
            bot.send_media_group(chat_id, media)
            return  # Успешная отправка, выходим из функции
        except Exception as e:
            logging.error(f"Ошибка при отправке группы медиа (попытка {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:  # Если это не последняя попытка
                time.sleep(delay)  # Ждем перед повторной попыткой
            else:
                bot.send_message(chat_id, "Не удалось отправить изображения после нескольких попыток.")

def create_markup(question_number):
    markup = types.InlineKeyboardMarkup(row_width=6)
    buttons = [types.InlineKeyboardButton(letter, callback_data=f'answer_{question_number}_{letter}') for letter in
               ['А', 'Б', 'В', 'Г', 'Д', 'Е']]
    markup.add(*buttons)
    return markup

def create_position_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(position, callback_data=f'position_{position}') for position in
               questions['position']['options'].keys()]
    markup.add(*buttons)
    return markup

def create_department_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)  # Изменим row_width для удобства
    buttons = [types.InlineKeyboardButton(f"{dept} ({code})",
                                          callback_data=f'department_{code}') for code, dept in
               questions['department']['options'].items()]
    markup.add(*buttons)
    # Добавим кнопки "Готово" и "Сбросить"
    done_button = types.InlineKeyboardButton("Готово", callback_data='department_done')
    reset_button = types.InlineKeyboardButton("Сбросить", callback_data='department_reset')
    markup.add(done_button, reset_button)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_answers[user_id] = {'answers': [], 'fio': None, 'position': None, 'department': [], 'username': None}
    departments[user_id] = {dept: 0 for dept in 'М HR И Н П А'.split()}

    # Путь к изображению
    image_path = '/home/vlados/bot_for_im_in/photos_for_bot/first.png' # Предполагаем, что изображение называется start_image.png

    # Текст сообщения
    text = """<b>привет, я распорядитель-Алеша!</b>👒

моя задача простая: 
<i>разобраться какой отдел тебе стоит рассмотреть в качестве дальнейшего развития.</i>

<u>что такое отделы?</u>

– это команды внутри Программы, которые реализуют внутренние проекты. Они помогают руководителям округов в обеспечении строительства нашего большого сообщества!

дальше тебя ждет несколько вопросов, которые помогут узнать себя в контуре работы с отделами, и возможность оставить заявку на работу в команде.

<b>важно:</b> 
итоги теста могут не совпадать с тем отделом, куда ты решишь подать заявку.

<b>удачи</b>💗"""

    try:
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=text, parse_mode="HTML")
    except FileNotFoundError:
        logging.error(f"Image file not found: {image_path}")
        bot.send_message(message.chat.id, text, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error sending image: {e}")
        bot.send_message(message.chat.id, text, parse_mode="HTML")

    time.sleep(5)
    send_question(message.chat.id, 1)

@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_'))
def handle_answer(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if user_id not in user_locks:
        user_locks[user_id] = threading.Lock()

    if not user_locks[user_id].acquire(blocking=False):
        bot.answer_callback_query(call.id, "Пожалуйста, дождитесь обработки предыдущего ответа.")
        return

    try:
        _, question_number, answer = call.data.split('_')
        question_number = int(question_number)

        if user_id not in user_answers:
            user_answers[user_id] = {'answers': [], 'fio': None, 'position': None, 'department': [], 'username': None}
            departments[user_id] = {dept: 0 for dept in 'М HR И Н П А'.split()}

        department_mapping = answer_to_department if question_number < 5 else answer_to_department_last
        department = department_mapping[answer]

        user_answers[user_id]['answers'].append(department)
        departments[user_id][department] += 1

        if len(user_answers[user_id]['answers']) < 5:
            send_question(chat_id, len(user_answers[user_id]['answers']) + 1)
        else:
            # Тест завершен. Определяем отдел и отправляем результат
            most_common_department = max(departments[user_id], key=departments[user_id].get)
            send_department_result(chat_id, most_common_department)

            # Создаем кнопку для отправки заявки
            markup = types.InlineKeyboardMarkup()
            apply_button = types.InlineKeyboardButton("Оставить заявку", callback_data="get_fio")
            markup.add(apply_button)

            bot.send_message(chat_id, "Спасибо за прохождение теста! Нажмите кнопку, чтобы оставить заявку:", reply_markup=markup)

    except Exception as e:
        logging.error(f"Ошибка в handle_answer: {e}")
    finally:
        user_locks[user_id].release()

# Изменения здесь
@bot.callback_query_handler(func=lambda call: call.data == "get_fio")
def ask_fio(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Пожалуйста, введите ваше ФИО:")
    user_steps[chat_id] = "get_fio"  # Установим шаг пользователя

@bot.message_handler(func=lambda message: user_steps.get(message.chat.id) == "get_fio")
def get_fio(message):
    user_id = message.from_user.id
    user_answers[user_id]['username'] = message.from_user.username
    user_answers[user_id]['fio'] = message.text
    user_steps[message.chat.id] = None

    # Запрашиваем должность
    bot.send_message(message.chat.id, questions['position']['question'], reply_markup=create_position_markup(), parse_mode="Markdown")

#Изменения здесь
@bot.callback_query_handler(func=lambda call: call.data.startswith('position_'))
def handle_position(call):
    user_id = call.from_user.id
    position = call.data.split('_')[1]
    user_answers[user_id]['position'] = position

    # Запрашиваем отдел
    user_answers[user_id]['department'] = []  # Инициализируем список выбранных отделов
    bot.send_message(call.message.chat.id, questions['department']['question'], reply_markup=create_department_markup(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('department_'))
def handle_department_choice(call):
    user_id = call.from_user.id
    department_code = call.data.split('_')[1]

    if user_id not in selected_departments:
        selected_departments[user_id] = []

    if department_code == 'done':
        # Пользователь закончил выбор отделов
        if not selected_departments[user_id]:
            bot.answer_callback_query(call.id, "Пожалуйста, выберите хотя бы один отдел.")
            return

        user_answers[user_id]['department'] = selected_departments[user_id]
        # Предпросмотр и подтверждение
        show_confirmation(call.message)
    elif department_code == 'reset':
        # Сброс выбора отделов
        selected_departments[user_id] = []
        bot.answer_callback_query(call.id, "Выбор отделов сброшен.")
    else:
        # Добавляем или удаляем отдел из списка выбранных
        if department_code in selected_departments[user_id]:
            selected_departments[user_id].remove(department_code)
            bot.answer_callback_query(call.id, f"Отдел {department_code} удален из списка.")
        else:
            selected_departments[user_id].append(department_code)
            bot.answer_callback_query(call.id, f"Отдел {department_code} добавлен в список.")

    # Проверяем, изменилась ли разметка перед обновлением
    new_markup = create_department_markup()
    current_markup = call.message.reply_markup

    if new_markup.to_dict() != current_markup.to_dict():
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=new_markup
        )

def show_confirmation(message):
    user_id = message.chat.id
    # Формируем текст для предпросмотра
    fio = user_answers[user_id]['fio']
    position = user_answers[user_id]['position']
    departments_str = ", ".join([questions['department']['options'][code] for code in user_answers[user_id]['department']])

    text = f"Подтвердите ваши данные:\n\nФИО: {fio}\nДолжность: {position}\nОтделы: {departments_str}"

    # Создаем кнопки "Подтвердить" и "Изменить"
    markup = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton("Подтвердить", callback_data="confirm_data")
    edit_button = types.InlineKeyboardButton("Изменить", callback_data="edit_data")
    markup.add(confirm_button, edit_button)

    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_data")
def handle_confirm_data(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Получаем список выбранных отделов
    selected_departments_str = ", ".join(user_answers[user_id]['department'])

    if user_id not in user_department_sent or not user_department_sent[user_id]:
        max_count = max(departments[user_id].values())
        suitable_departments = [key for key, value in departments[user_id].items() if value == max_count]

        # Формируем строку с ответами на вопросы теста
        test_answers = ", ".join(user_answers[user_id]['answers'])

        # Формируем строку с подходящими отделами
        suitable_depts_str = ", ".join(suitable_departments)

        user_department_sent[user_id] = True

        # Расширенная запись данных в Google Sheets
        values = [
            [
                user_answers[user_id]['username'],
                user_answers[user_id]['fio'],
                user_answers[user_id]['position'],
                selected_departments_str,  # Выбранные отделы
                test_answers,  # Ответы на вопросы теста
                suitable_depts_str  # Подходящие отделы по результатам теста
            ],
        ]
        body = {
            'values': values
        }
        try:
            result = service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                valueInputOption="USER_ENTERED", body=body).execute()
            logging.info(
                f"Данные успешно добавлены в Google Sheets. {result.get('updates').get('updatedCells')} cells updated.")
            bot.send_message(chat_id, "*Спасибо, что проявляешь интерес к деятельности в Программе.* С тобой обязательно свяжутся 💗", parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Ошибка при добавлении данных в Google Sheets: {e}")
            bot.send_message(chat_id, "Произошла ошибка при сохранении ваших данных.")
    else:
        bot.send_message(chat_id, "Информация об отделах уже была отправлена ранее.")

@bot.callback_query_handler(func=lambda call: call.data == "edit_data")
def handle_edit_data(call):
    # Возвращаемся к запросу ФИО (начало анкеты)
    bot.send_message(call.message.chat.id, "Пожалуйста, введите ваше ФИО:")
    user_steps[call.message.chat.id] = "get_fio"  # Установим шаг пользователя

def send_department_result(chat_id, department_code):
    if department_code in department_descriptions:
        department_info = department_descriptions[department_code]
        description = department_info['description']

        # Получаем путь к изображению из нового словаря
        if department_code in department_images:
            image_path = department_images[department_code]
        else:
            logging.error(f"Image path not found for department code: {department_code}")
            bot.send_message(chat_id, "К сожалению, не удалось найти картинку для отдела.")
            return

        try:
            with open(image_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=description, parse_mode="Markdown")
        except FileNotFoundError:
            logging.error(f"Image file not found: {image_path}")
            bot.send_message(chat_id, "К сожалению, не удалось отправить картинку с описанием отдела.")
        except Exception as e:
            logging.error(f"Error sending department result: {e}")
            bot.send_message(chat_id, "Произошла ошибка при отправке информации об отделе.")
    else:
        bot.send_message(chat_id, "К сожалению, не удалось определить подходящий отдел.")

if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except Exception as e:
        logging.error(f"Bot polling error: {e}")
