# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-05 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0004_auto_20171104_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_creation', models.DateField(auto_now_add=True, verbose_name='Дата создания заказа')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('telegram_user_id', models.IntegerField(unique=True, verbose_name='Telegram User ID')),
            ],
            options={
                'verbose_name': 'Работника компании',
                'verbose_name_plural': 'Работники компании',
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_app.Workers', to_field='telegram_user_id', verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='food',
            name='order',
            field=models.ManyToManyField(to='django_app.Orders'),
        ),
    ]