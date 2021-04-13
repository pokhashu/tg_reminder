import telebot
import config
import datetime
import time as t
import json

bot = telebot.TeleBot(config.TOKEN)

with open('db.json', 'r', encoding='utf-8') as db:
    DB = json.load(db)
done = []

while True:
    for chat_id in DB:
        for el in DB[chat_id][0]:
            if el == str(datetime.datetime.now().time())[0:5:1]:
                bot.send_message(chat_id, 'Вы просили напомнить: ' + DB[chat_id][0][el])
                del DB[chat_id][0][el]
                with open('db.json', 'w', encoding='utf-8') as db:
                    db.write(json.dumps(DB, ensure_ascii=False))
                break
    with open('db.json', 'r', encoding='utf-8') as db:
        DB = json.load(db)
    t.sleep(54)
