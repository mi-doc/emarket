# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-28 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0018_auto_20180128_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='diagonal',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=2, null=True),
        ),
    ]
