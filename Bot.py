#Импорт модулей
import telebot
import time
import os

#Связь с токеном и создание бота
token = os.environ.get("TOKEN")
bot = telebot.TeleBot(token)

all = {}

#/idea
@bot.message_handler(commands=["idea"])
def idea_message(message):
    text1 = message.text[5::]
    if text1 == '':
        bot.send_message(message.chat.id, "Вы не ввели идею!")
    else:
        bot.send_message("522487188", "Идея от: " + message.from_user.first_name + "\nid: " + str(message.from_user.id) + "\nИдея:" + text1)
        bot.send_message(message.chat.id, "Идея отправлена разработчику.")

#/help
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "/idea текст - предложить свою идею по улучшению бота\n/dz - узнать абсолютно всё дз на данный момент\n/dzs дата - узнать дз на указанную дату")

#new_dz
@bot.message_handler(commands=["new_dz"])
def new_dz_message(message):
    if message.from_user.id != 522487188:
        bot.send_message(message.chat.id, "У вас нет прав.")
    else:
        date = message.text[8:18]
        text = message.text[19::]
        if date != '' and text != '':
            all.update({date:text})
            bot.send_message(message.chat.id, "Дз добавлено!\n" + "Дата: " + date + "\nСодержание: " + text)
        else:
            bot.send_message(message.chat.id, "Ошибка!")

#dz
@bot.message_handler(commands=["dz"])
def dz_message(message):
    global all
    if len(all.keys()) != 0:
        s = ''
        for key, val in all.items():
            s += key + "\n" + val + "\n\n"
        bot.send_message(message.chat.id, s)
    else:
        bot.send_message(message.chat.id, "Нет дз)")

#dzs
@bot.message_handler(commands=["dzs"])
def dzs_message(message):
    date = message.text[5::]
    if date != '':
        global all
        if date in all.keys():
            bot.send_message(message.chat.id, all.get(date))
        else:
            bot.send_message(message.chat.id, "Даты не существует.")
    else:
        bot.send_message(message.chat.id, "Ошибка")

#delete_dz
@bot.message_handler(commands=["delete_dz"])
def delete_dz_message(message):
    global all
    if message.from_user.id != 522487188:
        bot.send_message(message.chat.id, "У вас нет прав.")
    else:
        date = message.text[11::]
        if date != '':
            if date in all.keys():
                all.pop(date)
                bot.send_message(message.chat.id, date + " осталось без дз(")
            else:
                bot.send_message(message.chat.id, "Даты не существует.")
        else:
            bot.send_message(message.chat.id, "Ошибка")
            
#time
@bot.message_handler(commands=["time"])
def time_message(message):
    bot.send_message(message.chat.id, str(start_time))
    a = int(time.time() - start_time)
    b,c,d = 0,0,0
    if a >= 60:
        b += 1
        a -= 60
    if b >= 60:
        c += 1
        b -= 60
    if c >= 24:
        d += 1
        c -= 24
    bot.send_message(message.chat.id, "Бот работает: " + str(d) + " дней " + str(c) + " часов " + str(b) + " минут " + str(a) + " секунд")

#Работа бота
bot.polling()
