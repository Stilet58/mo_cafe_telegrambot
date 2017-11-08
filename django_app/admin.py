from django.contrib import admin
from .models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price') #Сортировка отображения на странице
    list_display_links = ('name',)
    list_filter = ['category']  # Фильтр по категориям блюд
    search_fields = ['name']  # Текстовый поиск по названию блюда


class WorkersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name',  'last_name', 'telegram_user_id') #Сортировка отображения на странице
    list_display_links = ('first_name',  'last_name')
    search_fields = ['first_name', 'last_name']  # Текстовый поиск работника


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_of_creation',  'customer', 'get_dishes_list', 'sum') #Сортировка отображения на странице
    date_hierarchy = 'date_of_creation'  # Иерархический фильтр по дате заказа
    search_fields = ['customer__first_name', 'customer__last_name']  # Текстовый поиск заказов одного клиента


class ResultsMonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker',  'amount_per_month') #Сортировка отображения на странице
    list_display_links = ('worker',)
    search_fields = ['worker__first_name', 'worker__last_name']  # Текстовый поиск по работнику

admin.site.register(Food, FoodAdmin)
admin.site.register(Workers, WorkersAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(ResultsMonth, ResultsMonthAdmin)