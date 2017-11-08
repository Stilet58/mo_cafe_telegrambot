import sqlite3


class DBManager:

    def __init__(self, database):
        """Подключаемся к БД"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все пункты меню """
        with self.connection:
            return self.cursor.execute('SELECT * FROM django_app_food').fetchall()

    def select_all_workers(self):
        """ Получаем telegram user id всех работников компании """
        with self.connection:
            return self.cursor.execute('SELECT telegram_user_id FROM django_app_workers').fetchall()

    def insert_order(self, order_date, telegram_user_id, order_sum, order_numbers):
        """ Записываем заказ в БД """
        with self.connection:
            self.cursor.execute('INSERT INTO django_app_orders (date_of_creation, customer_id, sum )'
                                'VALUES (?, ?, ?)', (order_date, telegram_user_id, order_sum))
            last_id = self.cursor.lastrowid

            """Записываем заказанные блюда в заказ"""
            for i in range(0, len(order_numbers), 1):
                self.cursor.execute('INSERT INTO django_app_orders_dishes (orders_id, food_id)'
                                    'VALUES (?, ?)', (last_id, order_numbers[i]))

    def select_month_results(self, beginning_month, end_month):
        """ Получаем все заказы за текущий или предыдущий месяц """
        with self.connection:
            return self.cursor.execute('SELECT sum, customer_id FROM django_app_orders WHERE date_of_creation >= ? '
                                       'AND date_of_creation <= ?', (beginning_month, end_month)).fetchall()

    def insert_month_results(self, month_results):
        """ Записываем итоги месяца в БД """
        with self.connection:
            for i in range(0, len(month_results), 1):
                self.cursor.execute('INSERT INTO django_app_resultsmonth (amount_per_month, worker_id)'
                                    'VALUES (?, ?)', (month_results[i][1], month_results[i][0]))

    def delete_month_results(self):
        """ Удаляем предудыщие итоги месяца перед записью новых """
        with self.connection:
            self.cursor.execute('DELETE FROM django_app_resultsmonth')

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()