# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-28 18:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0021_auto_20180128_2138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='other_specifications',
        ),
    ]
