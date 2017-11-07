import telebot
from telegrambot.SQLighter import DBManager
from telegrambot import config
import datetime


bot = telebot.TeleBot(config.token)


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу сделать тебе заказ в Мо.Кафе. '
                                      'Для просмотра меню на сегодня введи /menu')

# Обработчик команды '/menu'.
@bot.message_handler(commands=['menu'])
def menu(message):
    # Подключаемся к БД
    db_worker = DBManager(config.database_name)
    all_data = db_worker.select_all()

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

    bot.send_message(message.chat.id, cafe_menu + 'Для заказа введи через запятую без пробела номера блюд, '
                                                  'которые хочешь заказать, и отправь мне. '
                                                  'Номера находятся слева от названий.')
    # Отсоединяемся от БД
    db_worker.close()


# Обработчик команды '/results current month'.
@bot.message_handler(commands=['results_current_month'])
def last_month_results(message):
    beginning_month = datetime.date.today()
    beginning_month = beginning_month.replace(day=1)
    end_month = datetime.date.today()
    next_month = end_month.month + 1
    end_month = end_month.replace(month=next_month, day=1) - datetime.timedelta(1)
    # Подключаемся к БД
    db_worker = DBManager(config.database_name)
    current_month_data = db_worker.select_month_results(beginning_month, end_month)
    print(current_month_data)


# Обработчик команд сделанного заказа.
@bot.message_handler(content_types=['text'])
def write_order(message):
    telegram_user_id = message.from_user.id
    list_food = message.text.split(',')
    order_date = datetime.date.today()
    order_numbers = sorted([int(item) for item in list_food])#Отсортированные номера блюд в заказе


    # Подключаемся к БД
    db_worker = DBManager(config.database_name)
    all_data = db_worker.select_all()
    dishes_numbers = []
    order_sum = 0

    for i in range(0, len(all_data), 1):
        dishes_numbers.append(all_data[i][0])

    for i in range(0, len(order_numbers), 1):
        if order_numbers[i] in dishes_numbers:
            for j in range(0, len(all_data), 1):
                if all_data[j][0] == order_numbers[i]:
                    order_sum += all_data[j][2]
                else:
                    continue
        else:
            order_sum = 0
            break

    if order_sum == 0:
        bot.send_message(message.chat.id, 'Возникла ошибка. Одного или нескольких номеров блюд нет в меню. '
                                          'Попробуй ввести и отправить заказ ещё раз.')
    else:
        bot.send_message(message.chat.id, 'Заказ принят. Cумма заказа ' + str(order_sum) + ' руб.')
        db_worker.insert_order(order_date, telegram_user_id, order_sum, order_numbers)
    # Отсоединяемся от БД
    db_worker.close()


if __name__ == '__main__':
     bot.polling(none_stop=True)

