# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-16 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0006_auto_20171215_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
