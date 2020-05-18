from peewee import *
import random
import os

passe = os.environ.get('SQL_pass')
db = PostgresqlDatabase('telebot', user='van4o2', password=passe, host='213.219.214.91', port=5432)


class BaseModel(Model):
    """Создание базовой модели"""

    class Meta:
        database = db

class request_answer(BaseModel):
    """"Вопрос - ответ, БД"""
    request = TextField()
    answer1 = TextField()
    answer2 = TextField()
    answer3 = TextField()
    answer4 = TextField()
    id = AutoField()

    @staticmethod
    #Поиск ответа на заданный вопрос в базе
    def answer(req_ans):
        try:
            sel = request_answer.select().where(request_answer.request == req_ans)
            td = []
            print(sel)
            for i in sel:
                td.extend([i.answer1, i.answer2, i.answer3, i.answer4])
            ans_message = random.choice(td)
            return ans_message
        except BaseException as e:
            return False
            pass



class user_group(BaseModel):
    """База данных зарегистрированных пользователей"""
    id = AutoField()
    chat_id = BigIntegerField()
    user_id = BigIntegerField()
    user_name = FixedCharField()
    user_last_name = FixedCharField()
    birth_day = DateField()

    # @staticmethod
    # # Проверка в базе пользователя
    # def userEx(IdUser):
    #     try:
    #         sel = user_group.select().where(user_group.user_id == IdUser).get()
    #         return True
    #     except DoesNotExist as de:
    #         pass

    @staticmethod
    #Добавить пользователя
    def add_user(chatId, userId, user_name, user_last_name, birth_day):
        try:
            sel = user_group.select().where(user_group.user_id == userId).get()

            return f'Ошибка \nПользователь с таким ID уже существует!'
        except DoesNotExist as de:
            nos = user_group(
                chat_id=chatId,
                user_id=userId,
                user_name=user_name,
                user_last_name=user_last_name,
                birth_day=birth_day)
            nos.save()
            return f'Вы успешно зарегистрированы!'

    @staticmethod
    #Проверка день рождения
    def birthDay(self):
        try:
            sel = user_group.select().where(user_group.birth_day == self).get()
            if str(sel.birth_day) == str(self):
                return f"Сегодня день рождения у '{sel.user_name} {sel.user_last_name.replace('None', '')}'!!!\n" \
                       f"Поздравляем!!!\n" \

            else:
                pass
        except Exception:
            return False
