#Импорт модулей
import telebot
import time
import os

#Связь с токеном и создание бота
token = os.environ.get("TOKEN")
bot = telebot.TeleBot(token)

start_time = time.time()

all = {}

#/idea
@bot.message_handler(commands=["idea"])
def idea_message(message):
    text1 = message.text[5::]
    if text1 == '':
        bot.send_message(message.chat.id, "Возникла ошибка.\nВозможная причина: Отсутствует текст.")
    else:
        bot.send_message("522487188", "Идея от: " + message.from_user.first_name + "\nid: " + str(message.from_user.id) + "\nИдея:" + text1)
        bot.send_message(message.chat.id, "Идея отправлена разработчику.")

#/help
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "/idea текст - предложить свою идею по улучшению бота\n/dz - узнать абсолютно всё дз на данный момент\n/dzs дата - узнать дз на указанную дату\n/time - показать время работы бота")
    bot.send_message("-363200275", "Имя: " + message.from_user.first_name + "\nid: " + str(message.from_user.id) + "\nСодержание: " + message.text)
    
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
            bot.send_message(message.chat.id, "Возникла ошибка.\nВозможные причины: Отсутствует дата или текст.")

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
        bot.send_message(message.chat.id, "Пусто.")
    bot.send_message("-363200275", "Имя: " + message.from_user.first_name + "\nid: " + str(message.from_user.id) + "\nСодержание: " + message.text)

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
        bot.send_message(message.chat.id, "Возникла ошибка.\nВозможная причина: Отсутствует дата.")
    bot.send_message("-363200275", "Имя: " + message.from_user.first_name + "\nid: " + str(message.from_user.id) + "\nСодержание: " + message.text)

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
    a = int(time.time() - start_time)
    b,c,d = 0,0,0
    if a >= 60:
        b += a // 60
        a -= a // 60 * 60
    if b >= 60:
        c += b // 60
        b -= b // 60 * 60
    if c >= 24:
        d += c // 24
        c -= c // 24 * 24
    bot.send_message(message.chat.id, "Бот работает: " + str(d) + " дней " + str(c) + " часов " + str(b) + " минут " + str(a) + " секунд")
    bot.send_message("-363200275", "Имя: " + message.from_user.first_name + "\nid: " + str(message.from_user.id) + "\nСодержание: " + message.text)

#logs
@bot.message_handler(content_types=["text"])
def text_message(message):
    bot.forward_message(message.chat.id,"-363200275",message.message_id)
    
#Работа бота
bot.polling()
