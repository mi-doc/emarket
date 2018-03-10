# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-09 16:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0009_auto_20180128_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinbasket',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]