from django.contrib import admin
from .models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price') #Сортировка отображения на странице
    list_display_links = ('name',)


class WorkersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name',  'last_name', 'telegram_user_id') #Сортировка отображения на странице
    list_display_links = ('first_name',  'last_name')

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_of_creation',  'customer', 'order', 'sum') #Сортировка отображения на странице

admin.site.register(Food, FoodAdmin)
admin.site.register(Workers, WorkersAdmin)
admin.site.register(Orders, OrdersAdmin)