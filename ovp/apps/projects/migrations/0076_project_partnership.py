# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-01-31 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0075_auto_20190121_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='partnership',
            field=models.BooleanField(default=False, verbose_name='Partnership'),
        ),
    ]
