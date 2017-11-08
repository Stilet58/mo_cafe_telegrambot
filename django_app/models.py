from django.db import models


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


#Модель работников компании
class Workers(models.Model):
    first_name = models.CharField('Имя', max_length=200)
    last_name = models.CharField('Фамилия', max_length=200)
    telegram_user_id = models.IntegerField('Telegram User ID', unique=True)

    class Meta:
        verbose_name = 'Работника компании'
        verbose_name_plural = 'Работники компании'

    def __str__(self):
        return self.last_name + ' ' + self.first_name


#Модель заказов
class Orders(models.Model):
    date_of_creation = models.DateField('Дата создания заказа')
    customer = models.ForeignKey(Workers, verbose_name='Клиент', on_delete=models.CASCADE, to_field='telegram_user_id')
    sum = models.IntegerField('Cумма заказа')
    dishes = models.ManyToManyField(Food, verbose_name='Блюда в заказе')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    #Отображение поля с заказнными блюдами в админке
    def get_dishes_list(self):
        dishes_list = self.dishes.get_queryset()
        dishes_str = ''
        for dishes in dishes_list:
            dishes_str += ', ' + dishes.name
        return dishes_str.lstrip(', ')

    # Название поля в админке
    get_dishes_list.short_description = 'Блюда в заказе'

    def __str__(self):
        return str(self.id)


#Модель потраченных сумм за месяц
class ResultsMonth(models.Model):
    worker = models.ForeignKey(Workers, verbose_name='Работник', on_delete=models.CASCADE, to_field='telegram_user_id')
    amount_per_month = models.IntegerField('Стоимость заказов за месяц')

    class Meta:
        verbose_name = 'Итог месяца'
        verbose_name_plural = 'Итоги месяца'

    def __str__(self):
        return str(self.worker)