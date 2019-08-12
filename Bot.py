#Импорт модулей
import telebot

#Связь с токеном и создание бота
bot = telebot.TeleBot("950234764:AAF8m_8vpMothwPryFNhbFka1F8s-MHTpE0")

#/start
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Я в работе)")

#Работа бота
bot.polling()
