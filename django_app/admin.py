from django.contrib import admin
from .models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price') #Сортировка отображения на странице
    list_display_links = ('name',)


class WorkersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name',  'last_name', 'telegram_user_id') #Сортировка отображения на странице
    list_display_links = ('first_name',  'last_name')


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_of_creation',  'customer', 'get_dishes_list', 'sum') #Сортировка отображения на странице


class ResultsMonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker',  'amount_per_month') #Сортировка отображения на странице
    list_display_links = ('worker',)

admin.site.register(Food, FoodAdmin)
admin.site.register(Workers, WorkersAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(ResultsMonth, ResultsMonthAdmin)