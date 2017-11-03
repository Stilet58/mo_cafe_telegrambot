import telebot


token = '464472587:AAHSfGXxyNe8kKLvG0ad1YdMtC4ZKRSgDs4'

bot = telebot.TeleBot(token)

# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Чтобы посмотреть меню, введите /menu')

'''
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)
'''
if __name__ == '__main__':
     bot.polling(none_stop=True)