import psycopg2
import random
import os
from contextlib import closing

passe = os.environ.get('SQL_pass')
# ДНИ РОЖДЕНИЯ
def birthday(th_date):
    baseEx()
    with closing(psycopg2.connect(dbname='telebot',
                                  user='van4o2',
                                  password=passe,
                                  host='213.219.214.91',
                                  port=5432)) as conn:  # Не забудь прописать хост
        with conn.cursor() as cursor:
            cursor.execute(
                f'''SELECT user_name, user_last_name, birth_day FROM public.user_group where birth_day = '{th_date}';''')
            user_ex = cursor.fetchall()
            if user_ex is not None:
                birs = (list(user_ex)[0][0].replace(' ', '') + " " + list(user_ex)[0][1].replace(' ', ''))
                print(birs)
                return birs
            else:
                return False


# создание базы и регистрация пользователей
def baseEx():
    with closing(psycopg2.connect(dbname='telebot',
                                  user='van4o2',
                                  password=passe,
                                  host='213.219.214.91',
                                  port=5432)) as conn:  # Не забудь прописать хост
        with conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS public.user_group (id serial, chat_id bigint NOT NULL, user_id bigint NOT NULL, user_name character(20) NOT NULL, user_last_name character(20) NOT NULL, birth_day date NOT NULL, PRIMARY KEY (id, user_id)); ALTER TABLE public.user_group OWNER to van4o2;''')
            conn.commit()
            conn.close()


# ПРОВЕРКА НА НАЛИЧИЕ ПОЛЬЗОВАТЕЛЯ В БАЗЕ


def reg_ex(user_id):
    baseEx()
    with closing(psycopg2.connect(dbname='telebot',
                                  user='van4o2',
                                  password=passe,
                                  host='213.219.214.91',
                                  port=5432)) as conn:  # Не забудь прописать хост
        with conn.cursor() as cursor:
            cursor.execute(f'''SELECT user_id FROM public.user_group where user_id = '{user_id}';''')
            user_ex = cursor.fetchall()
            if len(user_ex) >= 1:
                return False
            conn.close()


# создание базы и регистрация пользователей
def base_groupUser(chat_id, user_id, user_name, user_last_name, birth_day):
    baseEx()
    with closing(psycopg2.connect(dbname='telebot',
                                  user='van4o2',
                                  password=passe,
                                  host='213.219.214.91',
                                  port=5432)) as conn:  # Не забудь прописать хост
        with conn.cursor() as cursor:
            try:
                cursor.execute(f'''INSERT INTO public.user_group
                (chat_id, user_id, user_name, user_last_name, birth_day)
                VALUES ('{chat_id}','{user_id}','{user_name}','{user_last_name}','{birth_day}');''')
            except TypeError as er:
                print('Ошибка данных', er)
            conn.commit()
            conn.close()



# Вопрос-ответ из базы
def request_answer(self):
    with closing(psycopg2.connect(dbname='telebot',
                                  user='van4o2',
                                  password=passe,
                                  host='213.219.214.91',
                                  port=5432)) as conn:  # Не забудь прописать хост
        with conn.cursor() as cursor:
            baseEx()
            cursor.execute(
                f"SELECT answer1, answer2, answer3, answer4 FROM public.request_answer where request = '{self.lower().replace('!', '')}' ")
            self = cursor.fetchone()
            if self is not None:
                rand = random.randint(0, len(self) - 1)  # рандомим ответ из возможных вариантов
                return self[rand]
            else:
                return False
