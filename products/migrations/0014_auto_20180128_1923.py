# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-28 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20180128_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builtinmemory',
            name='value',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='ram',
            name='value',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
