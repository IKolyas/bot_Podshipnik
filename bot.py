import telebot
from telebot import types
import time as timer
import schedule
from config import token
from pars import Weather, pars_virus, parser_news
from pgSQL import request_answer, user_group
from config import day_th
from multiprocessing.context import Process
import datetime

bot_tb = telebot.AsyncTeleBot(token)


# heroku logs --tail --app polar-atoll-79899
# КОМАНДЫ
# - start
# - registration
# - virus
# - weather
# - news


# СТАРТ

@bot_tb.message_handler(commands=['start'])
def send_welcome(message):
    bot_tb.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKLV69A4QEgThXNn3yXtg8r5jOy_2YAAJFAAMNttIZjBr_PIJ9KtgZBA')
    timer.sleep(0.1)
    bot_tb.send_message(message.chat.id,
                        f"Привет, Люди! \nЯ бот. \nПока что я немного туповат, \
                     но мой создатель трудится над этим. \nВ общем чате для общения со мной используйте ' / '")


# - virus
@bot_tb.message_handler(commands=['virus'])
def virus_command(message):
    bot_tb.send_message(message.chat.id, pars_virus())


# - weather
@bot_tb.message_handler(commands=['weather'])
def weather_command(message):
    weather_city = Weather('Салехард')
    bot_tb.send_message(message.chat.id, weather_city.weather_in_day())
    del weather_city


# - Регистрация пользователей
@bot_tb.message_handler(commands=['registration'])
def reg_user(message):
    keyboard = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text="ДА", callback_data="yes")
    no_button = types.InlineKeyboardButton(text="Подумаю ...", callback_data="no")
    keyboard.add(yes_button, no_button)
    bot_tb.send_message(message.from_user.id, "Предлогаю тебе зарегистрироваться, это не займёт много времени...",
                        reply_markup=keyboard)


@bot_tb.callback_query_handler(func=lambda call: True)
def reg_key(call):
    if call.data == "yes":
        bot_tb.send_message(call.message.chat.id, "Введите дату рождения в формате: гггг-мм-чч, \n"
                                                  "Например: 1978-12-22")
        bot_tb.register_next_step_handler(call.message, get_birth)
    elif call.data == "no":
        bot_tb.send_message(call.message.chat.id, "Ок, я на связи")


def get_birth(message):
    birth_day = message.text.replace("/", "", 1)
    registration = user_group.add_user(message.chat.id, message.from_user.id, message.from_user.first_name,
                                       message.from_user.last_name, birth_day)
    bot_tb.send_message(message.chat.id, registration)


# - Новости
@bot_tb.message_handler(commands=['news'])
def send_news(message):
    bot_tb.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKL169A7a8k0SyrPkWW_6zF_fpFsU8AAI5AAMNttIZXzBAtjlTMTQZBA')
    timer.sleep(0.1)
    keyboard = types.InlineKeyboardMarkup()  # Больше новостей
    yes_button = types.InlineKeyboardButton(text="РИА НОВОСТИ",
                                            url=f"https://ria.ru/")
    keyboard.add(yes_button)
    bot_tb.send_message(message.chat.id, f"{parser_news()}", reply_markup=keyboard)
    timer.sleep(3)
    # Проверка, день рождения у зарегистрированных пользователей
    day = user_group.birthDay(day_th)  # day_th - текущая дата
    if day is not False:
        bot_tb.send_message(message.chat.id, day)
        bot_tb.send_sticker(message.chat.id, "CAACAgIAAxkBAAIKKl68gWv_U4RcCpIXEsIT9WDCqguWAAI7AAPRYSgLXdLS1ytBP50ZBA")


# - Обработчик текстовых сообщений
@bot_tb.message_handler(content_types=["text"])
def repeat_all_messages(message):
    message.text = message.text.replace("/", "")

    """информация по зараженным короновирусом(запрос в телеграме "вирус 'название города'")"""
    if message.text.lower().split(' ')[0] == 'вирус':
        bot_tb.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKIl675xAmpJrrYw7GNLDnyyUIYg9fAALIAQACVp29Ch5kbWu8BAS4GQQ')
        bot_tb.send_message(message.chat.id, pars_virus(message.text.lower().split(' ')[1]))

    """информация о погоде(запрос в телеграме "погода 'название города'")"""
    if message.text.lower().split(' ')[0] == 'погода':
        req_weather = message.text.lower().split(' ')[1]  # ИНФА ПО ПОГОДЕ с проверкой
        weather_answer = Weather(req_weather)
        bot_tb.send_message(message.chat.id, weather_answer.weather_in_day())
        del req_weather

    else:  # запрос к базе
        answer = request_answer.answer(message.text.lower())
        if answer is False:  # Если нет в базе, поиск в сети
            keyboard = types.InlineKeyboardMarkup()
            yes_button = types.InlineKeyboardButton(text="ДА",
                                                    url=f"https://yandex.ru/search/?text={message.text.replace(' ', '%20')}")
            keyboard.add(yes_button)
            bot_tb.send_message(message.chat.id, 'Не понимаю, о чём Вы? go Google...?', reply_markup=keyboard)
        else:
            bot_tb.send_message(message.chat.id, answer)


class TimerUs:
    def __init__(self):
        self.chat_id = 976733354

    def timer_news(self):
        # id = 976733354
        bot_tb.send_sticker(self.chat_id, 'CAACAgIAAxkBAAIKL169A7a8k0SyrPkWW_6zF_fpFsU8AAI5AAMNttIZXzBAtjlTMTQZBA')
        timer.sleep(0.1)
        keyboard = types.InlineKeyboardMarkup()  # Больше новостей
        yes_button = types.InlineKeyboardButton(text="РИА НОВОСТИ",
                                                url=f"https://ria.ru/")
        keyboard.add(yes_button)
        bot_tb.send_message(self.chat_id, f"{parser_news()}", reply_markup=keyboard)
        timer.sleep(3)
        # Проверка, день рождения у зарегистрированных пользователей
        day = user_group.birthDay(day_th)  # day_th - текущая дата
        if day is not False:
            bot_tb.send_message(self.chat_id, day)
            bot_tb.send_sticker(self.chat_id, "CAACAgIAAxkBAAIKKl68gWv_U4RcCpIXEsIT9WDCqguWAAI7AAPRYSgLXdLS1ytBP50ZBA")
    
    def timer_DMB(self):
        a = datetime.datetime.now()
        dday = datetime.datetime(2021, 10, 16)
        go_dmb = dday-a
        if (go_dmb.days == '1'):
            go_dmb = f'До дембея осталось {go_dmb.days} день'
        elif ('1' < str(go_dmb.days)[-1] < '5'): 
            go_dmb = f'До дембея осталось {go_dmb.days} дня'
        else:
            go_dmb = f'До дембея осталось {go_dmb.days} дней'
        bot_tb.send_message(self.chat_id, go_dmb)
        

class ScheduleMessage:

    @staticmethod
    def try_send():
        while True:
            schedule.run_pending()
            timer.sleep(30)

    @staticmethod
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send, args=())
        p1.start()


schedule.every().day.at("03:30").do(TimerUs().timer_news)
schedule.every().day.at("12:40").do(TimerUs().timer_news)
schedule.every().day.at("03:12").do(TimerUs().timer_DMB)

if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot_tb.infinity_polling(none_stop=True, interval=0.2)
    except:
        pass
