#Импорт модулей
import telebot
import time
import os

#Связь с токеном и создание бота
token = os.environ.get("TOKEN")
bot = telebot.TeleBot(token)

start_time = time.time()

all = {}
rasps = {"Понедельник":"1. ?\n2. ?\n3. ?\n4. ?"}

#/idea
@bot.message_handler(commands=["idea"])
def idea_message(message):
    if message.chat.type == "group":
        for admin in bot.get_chat_administrators(message.chat.id):
            if "950234764" in str(admin):
                text1 = message.text[5::]
                if text1 == '':
                    bot.send_message(message.chat.id, "Возникла ошибка.\nВозможная причина: Отсутствует текст.")
                else:
                    bot.send_message("522487188", "Идея от: " + message.from_user.first_name + "\nid: " + str(message.from_user.id) + "\nИдея:" + text1)
                    bot.send_message(message.chat.id, "Идея отправлена разработчику.")
                break
        else:
            bot.send_message(message.chat.id, "Мне нужны права администратора для этого действия.")
    else:
        text1 = message.text[5::]
        if text1 == '':
            bot.send_message(message.chat.id, "Возникла ошибка.\nВозможная причина: Отсутствует текст.")
        else:
            bot.send_message("522487188", "Идея от: " + message.from_user.first_name + "\nid: " + str(message.from_user.id) + "\nИдея:" + text1)
            bot.send_message(message.chat.id, "Идея отправлена разработчику.")
    bot.forward_message("-326941525", message.chat.id, message.message_id)
    
#/help
@bot.message_handler(commands=["help"])
def help_message(message):
    if message.chat.type == "group":
        for admin in bot.get_chat_administrators(message.chat.id):
            if "950234764" in str(admin):
                bot.send_message(message.chat.id, "/idea текст - предложить свою идею по улучшению бота\n/dz - узнать абсолютно всё дз на данный момент\n/dzs дата - узнать дз на указанную дату\n/time - показать время работы бота\n/help_developers - команды для проверенных людей")
                break
        else:
            bot.send_message(message.chat.id, "Мне нужны права администратора для этого действия.")
    else:
        bot.send_message(message.chat.id, "/idea текст - предложить свою идею по улучшению бота\n/dz - узнать абсолютно всё дз на данный момент\n/dzs дата - узнать дз на указанную дату\n/time - показать время работы бота\n/help_developers - команды для проверенных людей")
    bot.forward_message("-326941525", message.chat.id, message.message_id)
    
#/help_developers
@bot.message_handler(commands=["help_developers"])
def help_developers_message(message):
    if message.chat.type == "group":
        for admin in bot.get_chat_administrators(message.chat.id):
            if "950234764" in str(admin):
                if message.from_user.id == 522487188:
                    bot.send_message(message.chat.id, "/new_dz дата текст - создать новое дз\n/delete_dz дата - удалить дз на определённую дату")
                    break
                else:
                    bot.send_message(message.chat.id, "У вас нет прав.")
                    break
        else:
            bot.send_message(message.chat.id, "Мне нужны права администратора для этого действия.")
    else:
        if message.from_user.id == 522487188:
            bot.send_message(message.chat.id, "/new_dz дата текст - создать новое дз\n/delete_dz дата - удалить дз на определённую дату")
        else:
            bot.send_message(message.chat.id, "У вас нет прав.")
    bot.forward_message("-326941525", message.chat.id, message.message_id)
    
            
    
#new_dz
@bot.message_handler(commands=["new_dz"])
def new_dz_message(message):
    global all
    if message.from_user.id != 522487188:
        bot.send_message(message.chat.id, "У вас нет прав.")
    else:
        date = message.text[8:18]
        text = message.text[19::]
        if date != '' and text != '':
            all.update({date:text})
            bot.send_message(message.chat.id, "Дз добавлено!\n" + "Дата: " + date + "\nСодержание: " + text)
            bot.send_message("-366936457", "Дз обновилось!\n" + str(all))
        else:
            bot.send_message(message.chat.id, "Возникла ошибка.\nВозможные причины: Отсутствует дата или текст.")
    bot.forward_message("-326941525", message.chat.id, message.message_id)

#dz
@bot.message_handler(commands=["dz"])
def dz_message(message):
    global all
    if message.chat.type == "group":
        for admin in bot.get_chat_administrators(message.chat.id):
            if "950234764" in str(admin):
                if len(all.keys()) != 0:
                    s = ''
                    for key, val in all.items():
                        s += key + "\n" + val + "\n\n"
                    bot.send_message(message.chat.id, s)
                else:
                    bot.send_message(message.chat.id, "Пусто.")
                break
        else:
            bot.send_message(message.chat.id, "Мне нужны права администратора для этого действия.")
    else:
        if len(all.keys()) != 0:
            s = ''
            for key, val in all.items():
                s += key + "\n" + val + "\n\n"
            bot.send_message(message.chat.id, s)
        else:
            bot.send_message(message.chat.id, "Пусто.")
    bot.forward_message("-326941525", message.chat.id, message.message_id)
   
#rasp
@bot.message_handler(commands=["rasp"])
def rasp_message(message):
    global rasps
    if message.chat.type == "group":
        for admin in bot.get_chat_administrators(message.chat.id):
                if "950234764" in str(admin):
                s = ''
                for key, val in rasps.items():
                    s += key + "\n" + val + "\n"
                bot.send_message(message.chat.id, s)
                break
        else:
            bot.send_message(message.chat.id, "Мне нужны права администратора для этого действия.")
     else:
         s = ''
         for key, val in rasps.items():
             s += key + "\n" + val + "\n"
         bot.send_message(message.chat.id, s)
     bot.forward_message("-326941525", message.chat.id, message.message_id)
         
#dzs
@bot.message_handler(commands=["dzs"])
def dzs_message(message):
    global all
    if message.chat.type == "group":
        for admin in bot.get_chat_administrators(message.chat.id):
            if "950234764" in str(admin):
                date = message.text[5::]
                if date != '':
                    if date in all.keys():
                        bot.send_message(message.chat.id, all.get(date))
                    else:
                        bot.send_message(message.chat.id, "Даты не существует.")
                else:
                    bot.send_message(message.chat.id, "Возникла ошибка.\nВозможная причина: Отсутствует дата.")
                break
        else:
            bot.send_message(message.chat.id, "Мне нужны права администратора для этого действия.")
    else:
        date = message.text[5::]
        if date != '':
            if date in all.keys():
                bot.send_message(message.chat.id, all.get(date))
            else:
                bot.send_message(message.chat.id, "Даты не существует.")
        else:
            bot.send_message(message.chat.id, "Возникла ошибка.\nВозможная причина: Отсутствует дата.")
    bot.forward_message("-326941525", message.chat.id, message.message_id)
    

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
                bot.send_message("-366936457", "Дз обновилось!\n" + str(all))
            else:
                bot.send_message(message.chat.id, "Даты не существует.")
        else:
            bot.send_message(message.chat.id, "Возникла ошибка.\nВозможная причина: Отсутствует дата.")
    bot.forward_message("-326941525", message.chat.id, message.message_id)
            
#time
@bot.message_handler(commands=["time"])
def time_message(message):
    global start_time
    if message.chat.type == "group":
        for admin in bot.get_chat_administrators(message.chat.id):
            if "950234764" in str(admin):
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
                break
        else:
            bot.send_message(message.chat.id, "Мне нужны права администратора для этого действия.")
    else:
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
    bot.forward_message("-326941525", message.chat.id, message.message_id)
            

#logs
@bot.message_handler(content_types=["text"])
def text_message(message):
    bot.forward_message("-326941525", message.chat.id, message.message_id)
    
#Работа бота
bot.polling()
