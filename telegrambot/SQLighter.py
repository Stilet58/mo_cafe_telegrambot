import sqlite3


class DBManager:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM django_app_food').fetchall()

    def insert_order(self, order_date, telegram_user_id, order_sum, order_numbers):
        """ Записываем заказ в БД """
        with self.connection:
            self.cursor.execute('INSERT INTO django_app_orders (date_of_creation, customer_id, sum )'
                                'VALUES (?, ?, ?)', (order_date, telegram_user_id, order_sum))
            last_id = self.cursor.lastrowid

            for i in range(0, len(order_numbers), 1):
                self.cursor.execute('INSERT INTO django_app_orders_dishes (orders_id, food_id)'
                                    'VALUES (?, ?)', (last_id, order_numbers[i]))

    def select_month_results(self, beginning_month, end_month):
        """ Получаем итоги текущего месяца """
        with self.connection:
            return self.cursor.execute('SELECT sum, customer_id FROM django_app_orders WHERE date_of_creation > ? '
                                       'AND date_of_creation < ?', (beginning_month, end_month)).fetchall()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()