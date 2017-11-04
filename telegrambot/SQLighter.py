import sqlite3


class DBManager:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM django_app_food').fetchall()


    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()