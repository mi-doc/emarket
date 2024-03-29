# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-24 08:25
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0010_auto_20171217_1234'),
        ('orders', '0003_auto_20171211_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInBasket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nmb', models.IntegerField(default=1)),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order',
                 models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='orders.Order')),
                ('product',
                 models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='products.Product')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]
