# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-01 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0077_auto_20190204_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='chat_enabled',
            field=models.BooleanField(default=False, verbose_name='Chat Enabled'),
        ),
    ]
