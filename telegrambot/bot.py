import telebot
import sqlite3


token = '464472587:AAHSfGXxyNe8kKLvG0ad1YdMtC4ZKRSgDs4'
database_name = 'db.sqlite3'

bot = telebot.TeleBot(token)
connection = sqlite3.connect(database_name)
cursor = connection.cursor()
all_data = cursor.execute('SELECT * FROM django_app_food').fetchall()
print(all_data)


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Чтобы посмотреть меню, введите /menu')

'''
@bot.message_handler(commands=['menu'])
def menu(message):
    # Подключаемся к БД
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    all_data = cursor.execute('SELECT * FROM django_app_food').fetchall()
    bot.send_message(message.chat.id, all_data)
    # Отсоединяемся от БД
    connection.close()
'''
'''
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)
'''
if __name__ == '__main__':
     bot.polling(none_stop=True)