import telebot
from telegrambot.SQLighter import DBManager
from telegrambot import config
from django_app.models import *
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mo_cafe_telegrambot.settings")
django.setup()


bot = telebot.TeleBot(config.token)


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу сделать тебе заказ в Мо.Кафе. '
                                      'Для просмотра меню на сегодня введи /menu')


@bot.message_handler(commands=['menu'])
def menu(message):
    # Подключаемся к БД
    #db_worker = DBManager(config.database_name)
    all_data = Food.objects.all()#db_worker.select_all()
    print(all_data)
'''
    cafe_menu = ''
    arr_category = ['salads', 'first_meal', 'second_courses', 'garnishes', 'dessert', 'beverages']
    arr_category_rus = ['Салаты', 'Первые блюда', 'Вторые блюда', 'Гарниры', 'Десерты', 'Напитки']

    for j in range(0, len(arr_category), 1):
        cafe_menu = cafe_menu + arr_category_rus[j] + '\n'
        for i in range(0, len(all_data), 1):
            if all_data[i][3] == arr_category[j]:
                cafe_menu = cafe_menu + str(all_data[i][0]) + ' - ' + all_data[i][1] + ' - ' + str(all_data[i][2]) + 'р.\n'
            else:
                continue
        cafe_menu = cafe_menu + '\n'

    bot.send_message(message.chat.id, cafe_menu + 'Для заказа введи через запятую номера блюд, '
                                                  'которые хочешь заказать, и отправь мне. '
                                                  'Номера находятся слева от названий.')
    # Отсоединяемся от БД
    #db_worker.close()
'''

if __name__ == '__main__':
     bot.polling(none_stop=True)