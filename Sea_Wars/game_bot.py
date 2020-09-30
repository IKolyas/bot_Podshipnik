import telebot
from createArena import Arena
from telebot import types
import os
import shutil

from PIL import Image, ImageDraw, ImageFont
import sys

bot = telebot.TeleBot("1237586627:AAEAHJRObYll6jbvzyV5gULUVobQOoy5bAo")
playersID = [1111924759]

def add_user(userID):
    f = open('players.txt', 'w')
    f.write(f'{userID},')
    f.close()


class Users:
    player1 = None
    player1ID = None

    player2 = None
    player2ID = None

    def search_players(self, message):
        self.player1ID = message.from_user.id
        self.player1 = Arena()
        for user in playersID:
            if user != message.from_user.id:
                keyboard = types.InlineKeyboardMarkup()
                yes_button = types.InlineKeyboardButton(text="ДА", callback_data="yes")
                no_button = types.InlineKeyboardButton(text="НЕТ", callback_data="no")
                keyboard.add(yes_button, no_button)
                bot.send_message(user, f'Игрок {message.from_user.id} приглошает Вас в игру "Морской бой"!',
                                 reply_markup=keyboard)
        bot.send_message(message.from_user.id, 'Ожидаем второго игрока...')

    def add_player(self, call):
        if call.data == "yes":
            if self.player2ID is None:
                self.player2 = Arena()
                self.player2ID = call.from_user.id
                self.create_duel()

            else:
                bot.send_message(call.from_user.id, "Игрок уже найден!")
            # bot.register_next_step_handler(call.message, get_birth)
        if call.data == "no":
            bot.send_message(call.from_user.id, "Ок, я на связи")
        if call in self.player1.col:
            self.game(call)

    def create_duel(self):
        path = f'duels/{self.player1ID}_{self.player2ID}'
        try:
            os.mkdir(path)
        except Exception:
            pass
        self.player1.boardOwn.to_csv(f'{path}/{self.player1ID}o.csv')
        self.player1.boardShelling.to_csv(f'{path}/{self.player1ID}s.csv')
        self.player2.boardOwn.to_csv(f'{path}/{self.player2ID}o.csv')
        self.player2.boardShelling.to_csv(f'{path}/{self.player2ID}s.csv')
        shutil.copyfile("img/board.png", f"{path}/{self.player1ID}s.png")
        shutil.copyfile("img/board.png", f"{path}/{self.player2ID}s.png")
        self.point(self.player1, self.player1.boardOwn, path, self.player1ID)
        self.point(self.player2, self.player2.boardOwn, path, self.player2ID)

        self.update_Board()

        bot.send_message(self.player1ID, 'Стреляй!')

    def update_Board(self):
        path = f'duels/{self.player1ID}_{self.player2ID}'
        self.point(self.player1, self.player1.boardOwn, path, self.player1ID)
        self.point(self.player2, self.player2.boardOwn, path, self.player2ID)
        # BOARDS1
        bot.send_message(self.player1ID, f'Ваша доска')
        bot.send_photo(self.player1ID, open(f'{path}/{self.player1ID}o.png', 'rb'))
        bot.send_message(self.player1ID, f'Доска противника')
        bot.send_photo(self.player1ID, open(f'{path}/{self.player1ID}s.png', 'rb'))
        # BOARDS2
        bot.send_message(self.player2ID, f'Ваша доска')
        bot.send_photo(self.player2ID, open(f'{path}/{self.player2ID}o.png', 'rb'))
        bot.send_message(self.player2ID, f'Доска противника')
        bot.send_photo(self.player2ID, open(f'{path}/{self.player2ID}s.png', 'rb'))

    @staticmethod
    def point(player, boardOwn, path, pID):

        try:
            imgOwn = Image.open("img/board.png")
        except Exception as e:
            print(e, "Unable to load image")
            sys.exit(1)
        drawOwn = ImageDraw.Draw(imgOwn)
        font = ImageFont.truetype("arial.ttf", size=52)

        sbX = 49
        sbY = 51
        for r in range(0, 10):
            for c in player.col:
                if boardOwn.loc[r, c] == player.shipLabel:
                    drawOwn.text((sbY * player.col.index(c) + sbY, sbX * r + sbX), player.shipLabel, font=font,
                                 fill='#8B00FF')
                    imgOwn.save(f'{path}/{pID}o.png')
                if boardOwn.loc[r, c] == player.hit:
                    drawOwn.text((sbY * player.col.index(c) + sbY, sbX * r + sbX), player.hit, font=font,
                                 fill='#8B00FF')
                    imgOwn.save(f'{path}/{pID}o.png')
                if boardOwn.loc[r, c] == player.missed:
                    drawOwn.text((sbY * player.col.index(c) + sbY, sbX * r + sbX), player.missed, font=font,
                                 fill='#8B00FF')
                    imgOwn.save(f'{path}/{pID}o.png')

        try:
            imgOwn = Image.open("img/board.png")
        except Exception as e:
            print(e, "Unable to load image")
            sys.exit(1)
        drawOwn = ImageDraw.Draw(imgOwn)
        font = ImageFont.truetype("arial.ttf", size=52)

        sbX = 49
        sbY = 51
        for r in range(0, 10):
            for c in player.col:
                if player.boardShelling.loc[r, c] == player.hit:
                    drawOwn.text((sbY * player.col.index(c) + sbY, sbX * r + sbX), player.hit, font=font,
                                 fill='#8B00FF')
                    imgOwn.save(f'{path}/{pID}s.png')
                if player.boardShelling.loc[r, c] == player.missed:
                    drawOwn.text((sbY * player.col.index(c) + sbY, sbX * r + sbX), player.missed, font=font,
                                 fill='#8B00FF')
                    imgOwn.save(f'{path}/{pID}s.png')

    def game(self, message):
        char = message.text[0]
        num = int(message.text[1])

        if not (char in self.player1.col) or num > 9:
            bot.send_message(message.from_user.id, 'Ошибка ввода точки обстрела!')
            return print('error')

        if message.from_user.id == self.player1ID:

            if self.player1.boardShelling.loc[num, char] == self.player1.hit \
                    or self.player1.boardShelling.loc[num, char] == self.player1.missed:
                bot.send_message(self.player1ID, 'Ты уже стрелял в эту точку!')
                return print('error')

            if self.player2.boardOwn.loc[num, char] == self.player2.shipLabel:
                bot.send_message(self.player1ID, 'Попадание!')
                bot.send_message(self.player2ID, f'В тебя попали! {message.text}')

                self.player1.boardShelling.loc[num, char] = self.player1.hit
                self.player2.boardOwn.loc[num, char] = self.player2.hit
                self.update_Board()
                bot.send_message(self.player1ID, 'Стреляй!')

            else:
                bot.send_message(self.player1ID, 'Мимо!')
                self.player1.boardShelling.loc[num, char] = self.player1.missed
                self.player2.boardOwn.loc[num, char] = self.player2.missed
                self.update_Board()
                bot.send_message(self.player2ID, 'Стреляй!')

        if message.from_user.id == self.player2ID:

            if self.player2.boardShelling.loc[num, char] == self.player2.hit \
                    or self.player2.boardShelling.loc[num, char] == self.player2.missed:
                bot.send_message(self.player2ID, 'Ты уже стрелял в эту точку!')
                return print('error')

            if self.player1.boardOwn.loc[num, char] == self.player1.shipLabel:
                bot.send_message(self.player2ID, 'Попадание!')
                bot.send_message(self.player1ID, f'В тебя попали! {message.text}')

                self.player2.boardShelling.loc[num, char] = self.player2.hit
                self.player1.boardOwn.loc[num, char] = self.player1.hit
                self.update_Board()
                bot.send_message(self.player2ID, 'Стреляй!')

            else:
                bot.send_message(self.player2ID, 'Мимо!')
                self.player2.boardShelling.loc[num, char] = self.player2.missed
                self.player1.boardOwn.loc[num, char] = self.player1.missed
                self.update_Board()
                bot.send_message(self.player1ID, 'Стреляй!')

        if not (self.player2.shipLabel in self.player2.boardOwn.values):
            bot.send_message(self.player1ID, 'Победа!')
            bot.send_message(self.player2ID, f'Ты проиграл!')
        if not (self.player1.shipLabel in self.player1.boardOwn.values):
            bot.send_message(self.player2ID, 'Победа!')
            bot.send_message(self.player1ID, f'Ты проиграл!')


newGame = Users()
тм

@bot.message_handler(commands=['start'])
def send_welcome(message):
    add_user(message.from_user.id)
    if not (message.from_user.id in playersID):
        playersID.append(message.from_user.id)
    newGame.search_players(message)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    if not (message.from_user.id in playersID):
        playersID.append(message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def ready_to_play(call):
    newGame.add_player(call)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    newGame.game(message)


if __name__ == '__main__':
    try:
        bot.infinity_polling(none_stop=True, interval=0.5)
    except:
        pass
