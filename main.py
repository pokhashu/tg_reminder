# -*- coding: utf-8 -*-

import telebot
import config
# import subprocess
import json

bot = telebot.TeleBot(config.TOKEN)

week = {
    'mn': [0, 0, 0, 0, 0, 0, 0, 0],
    'tu': [0, 0, 0, 0, 0, 0, 0, 0],
    'wn': [0, 0, 0, 0, 0, 0, 0, 0],
    'th': [0, 0, 0, 0, 0, 0, 0, 0],
    'fr': [0, 0, 0, 0, 0, 0, 0, 0],
    'sa': [0, 0, 0, 0, 0, 0, 0, 0],
    'sn': [0, 0, 0, 0, 0, 0, 0, 0]
}

done = []
tmp = []
with open('db.json', 'r', encoding='utf-8') as db:
    DB = json.load(db)


class Lesson:
    def __init__(self, name, place, time):
        self.name = name
        self.place = place
        self.time = time

        week[place][time - 1] = name


class Reminder:
    def __init__(self, text, time, user_id, username):
        global DB
        self.text = text
        self.time = time
        self.user_id = user_id
        self.username = username

        if user_id not in DB:
            DB[user_id] = [{}, [], 0]
        DB[user_id][0][time] = text
        DB[user_id][2] = username

        with open('db.json', 'w', encoding='utf-8') as base:
            base.write(json.dumps(DB, ensure_ascii=False))
        with open('db.json', 'r', encoding='utf-8') as base:
            DB = json.load(base)


i = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.add('Добавить напоминание 📆', 'Удалить напоминание 🗑', 'Мои напоминания 🗂', row_width=2)
    bot.send_message(message.chat.id, 'Пожалуйста, выберите действие', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def execute(message):
    if message.text == 'Добавить напоминание 📆':
        add_to_timetable(message)
    elif message.text == 'Удалить напоминание 🗑':
        del_from_timetable(message)
    elif message.text == 'Мои напоминания 🗂':
        msg = 'Вот все ваши напоминания: \n'
        num = 1
        for el in DB[str(message.chat.id)][0]:
            msg += str(num) + '. ' + DB[str(message.chat.id)][0][el] + '\n'
            num += 1
        bot.send_message(message.chat.id, msg)
        start_message(message)


def add_to_timetable(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Подскажите, во сколько вам напомнить? \n(например:  17:34) ', reply_markup=a)
    bot.register_next_step_handler(message, add_time)


def add_time(message):
    tmp.append(message.text)
    bot.send_message(message.chat.id, 'Что  вам напомнить?', reply_markup=None)
    bot.register_next_step_handler(message, add_text)


def add_text(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.add('Добавить напоминание 📆', 'Удалить напоминание 🗑', 'Мои напоминания 🗂', row_width=2)
    tmp.append(message.text)
    bot.send_message(message.chat.id, 'Напоминание установлено!', reply_markup=keyboard)
    q = Reminder(tmp.pop(), tmp.pop(), str(message.chat.id), message.from_user.username)
    print(q)
    del q


def del_from_timetable(message):
    if DB[str(message.chat.id)][0]:
        reply = telebot.types.InlineKeyboardMarkup(row_width=1)
        for el in DB[str(message.chat.id)][0].keys():
            reply.add(telebot.types.InlineKeyboardButton(DB[str(message.chat.id)][0][el],
                                                         callback_data=el + DB[str(message.chat.id)][0][el]))
        bot.send_message(message.chat.id, 'Какое напоминание вы хотите удалить?', reply_markup=reply)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.add('Добавить напоминание 📆', 'Удалить напоминание 🗑', 'Мои напоминания 🗂', row_width=2)
        bot.send_message(message.chat.id, 'На данный момент список ваших напоминаний пуст', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def del_callback_inline(callback):
    global DB

    for el in DB[str(callback.message.chat.id)][0].keys():
        if callback.data == el + DB[str(callback.message.chat.id)][0][el]:
            del DB[str(callback.message.chat.id)][0][el]
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  text='Напоминание успешно удалено!', reply_markup=None)
            break
    with open('db.json', 'w', encoding='utf-8') as base:
        base.write(json.dumps(DB, ensure_ascii=False))
    with open('db.json', 'r', encoding='utf-8') as base:
        DB = json.load(base)


@bot.message_handler(commands=['admin_2903'])
def admin(message):
    print(message)


if __name__ == '__main__':
    # infinity_polling()
    bot.infinity_polling()

# https://habr.com/ru/post/462905/
