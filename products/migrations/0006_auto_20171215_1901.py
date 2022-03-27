# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-15 16:01
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005_productimage_is_main'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operational_system',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ОС',
                'verbose_name_plural': 'ОС',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='os',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    to='products.Operational_system'),
            preserve_default=False,
        ),
    ]
