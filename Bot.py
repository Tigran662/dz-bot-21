import telebot
import pymongo
from telebot import types
import os

mm = os.environ.get("Mongo")
tt = os.environ.get("TOKEN")
my_client = pymongo.MongoClient(mm)
bot = telebot.TeleBot(tt)

my_database = my_client.dz
my_collection = my_database.dz

my_database2 = my_client.rasp
my_collection2 = my_database2.rasp

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "/dz - узнать дз\n/rasp - показать расписание")
    bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)

@bot.message_handler(commands=["newdz"])
def newdz_message(message):
    if message.from_user.id == 522487188:
        date = message.text[7:21]
        text = message.text[22::]
        if date != "" and text != "":
            my_cursor = my_collection.find()
            for item in my_cursor:
                if item["date"] == date:
                    my_collection.update_one({"text":item["text"]},{"$set":{"text":item["text"]+"\n"+"• " + text + "\n"}})
                    bot.send_message(message.chat.id, "Дз обновлено")
                    break
            else:
                my_collection.insert_one({"date": date, "text": "• " + text + "\n"})
                bot.send_message(message.chat.id, "Дз создано")
        else:
            bot.send_message(message.chat.id, "Дата или текст указаны неправильно")
    else:
        bot.send_message(message.chat.id, "У вас нет прав.")

@bot.message_handler(commands=["dz"])
def url(message):
    my_cursor = my_collection.find()
    markup = types.InlineKeyboardMarkup()
    a = dict()
    for item in my_cursor:
        a.update({item["date"]:item["text"]})
    d1 = dict(sorted(a.items(), key = lambda x:x[0]))
    for key in d1.keys():
        btn_my_site=types.InlineKeyboardButton(text=str(key),callback_data=key)
        markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Выберите дату", reply_markup = markup)
    bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    my_cursor = my_collection.find()
    for item in my_cursor:
        if call.message:
            if call.data == item["date"]:
                try:
                    bot.send_message(call.from_user.id, item["date"] + "\n\n" + item["text"])
                except:
                    bot.send_message(call.message.chat.id, call.from_user.first_name + ", напишите мне в личку старт и я смогу отправлять вам сообщения!")
    my_cursor = my_collection2.find()
    for item in my_cursor:
        if call.message:
            if call.data == item["idch"]:
                try:
                    bot.send_message(call.from_user.id, "• " + item["ch"] + "\n\n" + item["rasp"])
                except:
                    bot.send_message(call.message.chat.id, call.from_user.first_name + ", напишите мне в личку старт и я смогу отправлять вам сообщения!")
    bot.send_message(-326941525, call.from_user.first_name + ": " + call.data)

@bot.message_handler(commands=["deletedz"])
def deletedz_message(message):
    if message.from_user.id == 522487188:
        a = message.text.split()
        my_cursor = my_collection.find()
        for item in my_cursor:
            if item["date"] == a[1]:
                my_collection.delete_one({"date":item["date"]})
                bot.send_message(message.chat.id, "Дз на дату " + a[1] + " удалено")
                break
        else:
            bot.send_message(message.chat.id, "Такой даты нет")
    else:
        bot.send_message(message.chat.id, "У вас нет прав.")

@bot.message_handler(commands=["send"])
def send1_message(message):
    if message.from_user.id == 522487188:
        bot.send_message(-1001219015757, message.text[6::])

@bot.message_handler(commands=["sendkl"])
def send1_message(message):
    if message.text[8::] != "":
        if message.from_user.id == 522487188:
            bot.send_message(-361703950, message.text[8::])
            bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)
    else:
        bot.send_message(message.chat.id, "Введите текст")

@bot.message_handler(commands=["set"])
def set_message(message):
    if message.from_user.id == 522487188:
        my_cursor = my_collection2.find()
        for item in my_cursor:
            if item["idch"] == "prosto":
                if item["val"] == "Числитель":
                    my_collection2.update_one({"idch":"prosto"},{"$set":{"val":"Знаменатель"}})
                    bot.send_message(message.chat.id,"Изменено на знаменатель")
                    break
                else:
                    my_collection2.update_one({"idch":"prosto"},{"$set":{"val":"Числитель"}})
                    bot.send_message(message.chat.id,"Изменено на числитель")
                    break

@bot.message_handler(commands=["rasp"])
def rasp_message(message):
    my_cursor = my_collection2.find()
    markup2 = types.InlineKeyboardMarkup()
    btn_my_site=types.InlineKeyboardButton(text="Понедельник",callback_data="Mon")
    markup2.add(btn_my_site)
    btn_my_site=types.InlineKeyboardButton(text="Вторник",callback_data="Tue")
    markup2.add(btn_my_site)
    btn_my_site=types.InlineKeyboardButton(text="Среда",callback_data="Wed")
    markup2.add(btn_my_site)
    btn_my_site=types.InlineKeyboardButton(text="Четверг",callback_data="Thu")
    markup2.add(btn_my_site)
    btn_my_site=types.InlineKeyboardButton(text="Пятница",callback_data="Fri")
    markup2.add(btn_my_site)
    for item in my_cursor:
        if item["idch"] == "prosto":
            bot.send_message(message.chat.id, "Выберите день недели\nНа данный момент: " + item["val"], reply_markup = markup2)
            break
    bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)

@bot.message_handler(content_types=["text"])
def text_message(message):
    bot.send_message(-326941525, message.from_user.first_name + ": " + message.text)

bot.polling()
