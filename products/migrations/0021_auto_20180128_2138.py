# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-28 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0020_auto_20180128_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_camera',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Main camera (Mpx)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='built_in_memory',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Built in memory (Gb)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='diagonal',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=5, null=True,
                                      verbose_name='Diagonal (inches)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Discount (percent)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ram',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Ram (Gb)'),
        ),
    ]
