# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_auto_20170928_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='amount',
            field=models.IntegerField(default=20, verbose_name='Amount'),
        ),
    ]
