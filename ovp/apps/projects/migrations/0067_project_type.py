# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-05 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0066_auto_20181022_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[(1, 'normal'), (2, 'donation')], default=1, max_length=10, verbose_name='Project Type'),
        ),
    ]
