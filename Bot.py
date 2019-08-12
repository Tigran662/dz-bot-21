#Импорт модулей
import telebot
import os

#Связь с токеном и создание бота
token = os.environ.get("TOKEN")
bot = telebot.TeleBot(token)

#/start
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Я в работе!")
    
#/idea
@bot.message_handler(commands=["idea"])
def idea_message(message):
    text1 = message.text[5::]
    if text1 == '':
        bot.send_message(message.chat.id, "Вы не ввели идею!")
    else:
        bot.send_message("522487188", text1)

#Работа бота
bot.polling()
