import telebot
from telegrambot.SQLighter import DBManager
from telegrambot import config
import datetime

#Создаем бота
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
    all_data = db_worker.select_all()   #Делаем выборку всех пунктов меню

    cafe_menu = ''
    #Спиок для прохода по меню
    arr_category = ['salads', 'first_meal', 'second_courses', 'garnishes', 'dessert', 'beverages']
    #Список для формирования сообщения с меню
    arr_category_rus = ['Салаты', 'Первые блюда', 'Вторые блюда', 'Гарниры', 'Десерты', 'Напитки']

    #Формируем сообщение с меню для отправки клиенту
    for j in range(0, len(arr_category), 1):
        cafe_menu = cafe_menu + arr_category_rus[j] + '\n'

        for i in range(0, len(all_data), 1):
            if all_data[i][3] == arr_category[j]:
                cafe_menu = cafe_menu + str(all_data[i][0]) + ' - ' + all_data[i][1] + ' - ' + str(all_data[i][2]) + 'р.\n'
            else:
                continue

        cafe_menu = cafe_menu + '\n'
    #Отправляем меню клиенту
    bot.send_message(message.chat.id, cafe_menu + 'Для заказа введи через запятую без пробела номера блюд, '
                                                  'которые хочешь заказать, и отправь мне. '
                                                  'Номера находятся слева от названий.')
    # Отсоединяемся от БД
    db_worker.close()


# Обработчик команды '/results current month'.
@bot.message_handler(commands=['results_current_month'])
def write_results_current_month(message):

    if message.from_user.id == config.admin_tlegram_id:
        #Определяем начало и конец текущего месяца
        beginning_month = datetime.date.today()
        beginning_month = beginning_month.replace(day=1)
        end_month = datetime.date.today()
        next_month = end_month.month + 1
        end_month = end_month.replace(month=next_month, day=1) - datetime.timedelta(1)

        # Подключаемся к БД
        db_worker = DBManager(config.database_name)
        all_workers = db_worker.select_all_workers()#Получаем выборку всех работников из БД
        # Выборка всех заказов за текущий месяц
        current_month_orders = db_worker.select_month_results(beginning_month, end_month)
        month_results = []

        #Создаем список всех работников с суммами, потраченными за месяц
        for i in range(0, len(all_workers), 1):
            amount_per_month = 0

            for j in range(0, len(current_month_orders), 1):
                if current_month_orders[j][1] == all_workers[i][0]:
                    amount_per_month += current_month_orders[j][0]
                else:
                    continue

            one_worker_results = [all_workers[i][0], amount_per_month]
            month_results.append(one_worker_results)

        db_worker.delete_month_results() #Удаляем предыдущие итоги из таблицы
        db_worker.insert_month_results(month_results) #Записываем итоги в таблицу
        bot.send_message(message.chat.id, 'Итоги текущего месяца записаны в базу данных.')

    else:
        bot.send_message(message.chat.id, 'Извини, у тебя нет прав для выполнения этой команды.')


# Обработчик команды '/results previous month'.
@bot.message_handler(commands=['results_previous_month'])
def write_results_previous_month(message):

    if message.from_user.id == config.admin_tlegram_id:
        #Определяем начало и конец прошедшего месяца
        beginning_month = datetime.date.today()
        previous_month = beginning_month.month - 1
        beginning_month = beginning_month.replace(month=previous_month, day=1)
        end_month = datetime.date.today()
        end_month = end_month.replace(day=1) - datetime.timedelta(1)

        # Подключаемся к БД
        db_worker = DBManager(config.database_name)
        all_workers = db_worker.select_all_workers() #Получаем выборку всех работников из БД
        # Выборка всех заказов за прошедший месяц
        current_month_orders = db_worker.select_month_results(beginning_month, end_month)
        month_results = []

        # Создаем список всех работников с суммами, потраченными за месяц
        for i in range(0, len(all_workers), 1):
            amount_per_month = 0

            for j in range(0, len(current_month_orders), 1):
                if current_month_orders[j][1] == all_workers[i][0]:
                    amount_per_month += current_month_orders[j][0]
                else:
                    continue

            one_worker_results = [all_workers[i][0], amount_per_month]
            month_results.append(one_worker_results)

        db_worker.delete_month_results() #Удаляем предыдущие итоги из таблицы
        db_worker.insert_month_results(month_results) #Записываем итоги в таблицу
        bot.send_message(message.chat.id, 'Итоги предыдущего месяца записаны в базу данных.')

    else:
        bot.send_message(message.chat.id, 'Извини, у тебя нет прав для выполнения этой команды.')


# Обработчик команд сделанного заказа.
@bot.message_handler(content_types=['text'])
def write_order(message):

    telegram_user_id = message.from_user.id #Id клиента сделавшего заказ
    list_food = message.text.split(',')
    order_date = datetime.date.today() #Дата заказа для записи в БД
    order_numbers = sorted([int(item) for item in list_food])#Отсортированные номера блюд в заказе

    # Подключаемся к БД
    db_worker = DBManager(config.database_name)
    all_data = db_worker.select_all() #Получаем все пункты меню
    dishes_numbers = []
    order_sum = 0

    #Номера блюд для дальнейшей проверки соответсвию меню
    for i in range(0, len(all_data), 1):
        dishes_numbers.append(all_data[i][0])

    #Проверяем правилность заказа, если правильно, вычисляем его сумму
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
        #Записываем заказ в БД
        db_worker.insert_order(order_date, telegram_user_id, order_sum, order_numbers)
    # Отсоединяемся от БД
    db_worker.close()


if __name__ == '__main__':
     bot.polling(none_stop=True)

