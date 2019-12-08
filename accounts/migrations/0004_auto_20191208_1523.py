# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-08 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='second_name',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
    ]
