import config
import telebot
from telebot import types
from db_logic import *

bot = telebot.TeleBot(config.TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
pars_button = types.KeyboardButton('Скачать данные с Wikipedia')
info_button = types.KeyboardButton('Ввести название города')
keyboard.add(pars_button, info_button)


@bot.message_handler(commands=["start"])
def start(message):
    """Функция главного меню после старта"""

    bot.send_message(message.chat.id, "Выберите что хотели бы сделать", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def choice(message):
    """Функция обработки нажатия клавиатуры"""
    if message.text == "Скачать данные с Wikipedia":
        insert_update_data()
        bot.send_message(message.chat.id, "Скачали данные из википедии")
    else:
        bot.send_message(message.chat.id, "Введите название города")
        bot.register_next_step_handler(message, get_city)


def get_city(message):
    """Функция получения города из БД"""
    city = message.text
    answer = get_data(city)
    # to_chat = f'Город: {answer[0]} имеет население {answer[1]} человек. Ссылка на вики: {answer[2]}'
    # print(to_chat)
    bot.send_message(message.chat.id, answer)
    bot.send_message(message.chat.id, "Что делаем дальше?", reply_markup=keyboard)


bot.polling(none_stop=True)

