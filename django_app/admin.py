from django.contrib import admin
from .models import Food


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',  'category', 'price') #Сортировка отображения на странице

admin.site.register(Food)