from multiprocessing.context import Process
import schedule
from bot import bot
import time as timer
from telebot import types
from pgSQL import user_group
from config import day_th
from pars import parser_news


class Timer:
    def __init__(self):
        self.chat_id = 976733354

    def timer_news(self):
        # id = 976733354
        bot.send_sticker(self.chat_id, 'CAACAgIAAxkBAAIKL169A7a8k0SyrPkWW_6zF_fpFsU8AAI5AAMNttIZXzBAtjlTMTQZBA')
        timer.sleep(0.1)
        keyboard = types.InlineKeyboardMarkup()  # Больше новостей
        yes_button = types.InlineKeyboardButton(text="РИА НОВОСТИ",
                                                url=f"https://ria.ru/")
        keyboard.add(yes_button)
        bot.send_message(self.chat_id, f"{parser_news()}", reply_markup=keyboard)
        timer.sleep(3)
        # Проверка, день рождения у зарегистрированных пользователей
        day = user_group.birthDay(day_th)  # day_th - текущая дата
        if day is not False:
            bot.send_message(self.chat_id, day)
            bot.send_sticker(self.chat_id, "CAACAgIAAxkBAAIKKl68gWv_U4RcCpIXEsIT9WDCqguWAAI7AAPRYSgLXdLS1ytBP50ZBA")


class ScheduleMessage:

    def try_send_schedule():
        while True:
            schedule.run_pending()
            timer.sleep(30)

    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()
