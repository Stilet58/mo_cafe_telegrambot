from django.db import models


#Модель для работников
class Workers(models.Model):
    first_name = models.CharField('Имя', max_length=200)
    last_name = models.CharField('Фамилия', max_length=200)
    telegram_user_id = models.IntegerField('Telegram User ID', unique=True)

    class Meta:
        verbose_name = 'Работника компании'
        verbose_name_plural = 'Работники компании'

    def __str__(self):
        return self.last_name + ' ' + self.first_name


#Модель для заказов
class Orders(models.Model):
    date_of_creation = models.DateField('Дата создания заказа', auto_now_add=True)
    customer = models.ForeignKey(Workers, verbose_name='Клиент', on_delete=models.CASCADE, to_field='telegram_user_id')
    order = models.CharField('Заказ', max_length=1000)
    sum = models.IntegerField('Cумма заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)



# Категории блюд
CATEGORY_FOOD = (
    ('salads', 'Cалаты'),
    ('first_meal', 'Первые блюда'),
    ('second_courses', 'Вторые блюда'),
    ('garnishes', 'Гарниры'),
    ('dessert', 'Десерты'),
    ('beverages', 'Напитки'),
    )


#Модель меню
class Food(models.Model):
    category = models.CharField('Категория', max_length=50, choices=CATEGORY_FOOD)
    name = models.CharField('Название', max_length=200)
    price = models.IntegerField('Цена')

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return str(self.name)