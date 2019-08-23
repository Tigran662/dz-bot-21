#Импорт модулей
import telebot
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
        else:
            bot.send_message(message.chat.id, "Ошибка!")

#dz
@bot.message_handler(commands=["dz"])
def dz_message(message):
    global all
    bot.send_message(message.chat.id, all)

#dzs
@bot.message_handler(commands=["dzs"])
def dzs_message(message):
    date = message.text[5::]
    if date != '':
        f = open("dz.txt", "r")
        a = f.read()
        f.close()
        b = []
        a = a.split("\n")
        for i in range(len(a)):
            if a[i] != "":
                b.append(a[i].split(";"))
        for i in b:
            if i[0] == date:
                s = ''
                for j in i:
                    s += j + "\n"
                bot.send_message(message.chat.id, s)
                break
        else:
            bot.send_message(message.chat.id, "Даты не существует!")
    else:
        bot.send_message(message.chat.id, "Ошибка")

#delete_dz
@bot.message_handler(commands=["delete_dz"])
def delete_dz_message(message):
    if message.from_user.id != 522487188:
        bot.send_message(message.chat.id, "У вас нет прав.")
    else:
        date = message.text[11::]
        if date != '':
            f = open("dz.txt", "r")
            a = f.read()
            f.close()
            b = []
            a = a.split("\n")
            for i in range(len(a)):
                if a[i] != "":
                    b.append(a[i].split(";"))
            for i in range(len(b)):
                if b[i][0] == date:
                    b.remove(b[i])
                    f = open("dz.txt", "w")
                    for i in b:
                        f.write(";".join(i)+"\n")
                    f.close()
                    bot.send_message(message.chat.id, date + " осталось без дз(")
                    break
            else:
                bot.send_message(message.chat.id, "Такой даты не существует!")
        else:
            bot.send_message(message.chat.id, "Ошибка")

#Работа бота
bot.polling()
