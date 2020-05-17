import telebot
import time as timer
import os
from pars import Weather
from pars import pars_virus, parser_news
from pgSQL import base_groupUser, reg_ex, birthday, request_answer
from config import day_th
from telebot import types
from datetime import datetime, date, time


token = os.environ.get('Bot_Toketn')
bot = telebot.AsyncTeleBot(token)


# КОМАНДЫ
# - start
# - registration
# - virus
# - weather
# - news

# СТАРТ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKLV69A4QEgThXNn3yXtg8r5jOy_2YAAJFAAMNttIZjBr_PIJ9KtgZBA')
    timer.sleep(0.1)
    bot.send_message(message.chat.id,
                     f"Привет, Люди! \nЯ бот. \nПока что я немного туповат, \
                     но мой создатель трудится над этим. \nВ общем чате для общения со мной используйте ' / '")

# - virus
@bot.message_handler(commands=['virus'])
def virus_command(message):
    bot.send_message(message.chat.id, pars_virus())


# - weather
@bot.message_handler(commands=['weather'])
def weather_command(message):
    weather_city = Weather('Салехард')
    bot.send_message(message.chat.id, weather_city.weather_in_day())
    del weather_city


'''Регистрация пользователей'''
@bot.message_handler(commands=['registration'])
def reg_user(message):
    if reg_ex(message.from_user.id) is False:
        bot.send_message(message.from_user.id, "Пользователь с таким ID уже зарегистрирован!")
    else:
        keyboard = types.InlineKeyboardMarkup()
        yes_button = types.InlineKeyboardButton(text="ДА", callback_data="yes")
        no_button = types.InlineKeyboardButton(text="Подумаю ...", callback_data="no")
        keyboard.add(yes_button, no_button)
        bot.send_message(message.from_user.id, "Предлогаю тебе зарегистрироваться, это не займёт много времени...",
                         reply_markup=keyboard)

№
@bot.callback_query_handler(func=lambda call: True)
def reg_key(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Ваше имя я уже знаю, введите дату рождения в формате: гггг-мм-чч, \n"
                                               "Например: 1978-12-22")
        bot.register_next_step_handler(call.message, get_birth)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Ок, я на связи")


def get_birth(message):
    birth_day = message.text.replace("/", "", 1)
    try:
        base_groupUser(message.chat.id, message.from_user.id, message.from_user.first_name,
                       message.from_user.last_name, birth_day)
        bot.send_message(message.chat.id, "Отлично, ты зарегистрирован!")
    except Exception as ex:
        bot.send_message(message.chat.id, "Ошибочка! Проверьте правильность вводимых данных.")


"""Новости"""
@bot.message_handler(commands=['news'])
def send_news(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKL169A7a8k0SyrPkWW_6zF_fpFsU8AAI5AAMNttIZXzBAtjlTMTQZBA')
    timer.sleep(0.1)
    keyboard = types.InlineKeyboardMarkup()                                             # Больше новостей
    yes_button = types.InlineKeyboardButton(text="РИА НОВОСТИ",
                                            url=f"https://ria.ru/")
    keyboard.add(yes_button)
    bot.send_message(message.chat.id, f"{parser_news()}", reply_markup=keyboard)
    timer.sleep(5)

    """Проверка, день рождения у зарегистрированных пользователей"""
    day = birthday(day_th)
    if day is not False:
        bot.send_message(message.chat.id, f"Сегодня день рождения у {day}! \nПоздравляем!")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKKl68gWv_U4RcCpIXEsIT9WDCqguWAAI7AAPRYSgLXdLS1ytBP50ZBA')

"""Обработчик текстовых сообщений"""
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    message.text = message.text.replace("/", "")

    """информация по зараженным короновирусом(запрос в телеграме "вирус 'название города'")"""
    if message.text.lower().split(' ')[0] == 'вирус':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKIl675xAmpJrrYw7GNLDnyyUIYg9fAALIAQACVp29Ch5kbWu8BAS4GQQ')
        bot.send_message(message.chat.id, pars_virus(message.text.lower().split(' ')[1]))

    """информация о погоде(запрос в телеграме "погода 'название города'")"""
    if message.text.lower().split(' ')[0] == 'погода':
        req_weather = message.text.lower().split(' ')[1] # ИНФА ПО ПОГОДЕ с проверкой
        weather_answer = Weather(req_weather)
        bot.send_message(message.chat.id, weather_answer.weather_in_day())
        del req_weather

    else:  # Запрос к базе
        answer = request_answer(message.text)
        if answer is False:  # Если нет в базе, поиск в сети
            keyboard = types.InlineKeyboardMarkup()
            yes_button = types.InlineKeyboardButton(text="ДА",
                                                    url=f"https://yandex.ru/search/?text={message.text.replace(' ', '%20')}")
            keyboard.add(yes_button)
            bot.send_message(message.chat.id, 'Не понимаю, о чём Вы? Может посмотрим в сети?', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, answer)


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True, interval=0.5)
