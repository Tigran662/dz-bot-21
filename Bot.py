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

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "/dz - узнать дз")
    bot.send_message(-326941525, "Гавночух унитаза по имени " + message.from_user.first_name + " написал " + message.text) 
    
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
    bot.send_message(-326941525, "Такому дерьму, как " + message.from_user.first_name + " понадобилось дз, вот же чмо)")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    name = call.from_user.first_name
    my_cursor = my_collection.find()
    for item in my_cursor:
        if call.message:
            if call.data == item["date"]:
                bot.send_message(call.message.chat.id, item["date"] + "\n\n" + item["text"])
                bot.send_message(-326941525, name + " узналo дз на " + call.data + ", наверное это чмо его не записало, в прочем, ничё нового =/")

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

@bot.message_handler(content_types=["text"])
def text_message(message):
    bot.send_message(-326941525, "Даунич с именем " + message.from_user.first_name + " написал " + message.text)

bot.polling()
