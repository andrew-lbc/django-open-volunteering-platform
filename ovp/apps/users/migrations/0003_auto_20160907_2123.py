# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160907_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='Slug'),
        ),
    ]
