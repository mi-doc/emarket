# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-16 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20171216_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]