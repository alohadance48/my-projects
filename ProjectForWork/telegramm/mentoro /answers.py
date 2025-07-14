import telebot
from telebot import types
import os

bot = telebot.TeleBot('')

TARGET_FILE_NAME = 'answer.png'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Получить ответы", callback_data='get_answers')
    markup.add(button)
    bot.send_message(message.chat.id, "Нажмите кнопку, чтобы получить ответы:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'get_answers')
def send_file(call):
    directory_path = 'path/to/your/files'
    file_path = os.path.join(directory_path, TARGET_FILE_NAME)

    if os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as file:
                bot.send_document(call.message.chat.id, file)
            bot.send_message(call.message.chat.id, "Файл успешно отправлен!")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Ошибка при отправке файла: {e}")
    else:
        bot.send_message(call.message.chat.id, f"Файл '{TARGET_FILE_NAME}' не найден.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
