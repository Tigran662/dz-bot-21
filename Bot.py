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
    bot.send_message(message.chat.id, message.chat.id)

#Работа бота
bot.polling()
