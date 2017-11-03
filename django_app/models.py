from django.db import models


#Модель меню
class Menu(models.Model):
    category = models.CharField('Категория', max_length=50)
    name = models.CharField('Название', max_length=200)
    price = models.IntegerField('Цена')

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return str(self.name)