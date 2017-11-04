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