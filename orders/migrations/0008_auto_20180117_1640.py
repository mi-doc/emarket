# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-17 13:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0007_productinbasket_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='productinbasket',
            options={'verbose_name': 'Product in basket', 'verbose_name_plural': 'Products in basket'},
        ),
        migrations.AlterModelOptions(
            name='productinorder',
            options={'verbose_name': 'Product in order', 'verbose_name_plural': 'Products in order'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Status', 'verbose_name_plural': 'Order status'},
        ),
    ]
