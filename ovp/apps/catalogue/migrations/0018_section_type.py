# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-11-09 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0017_auto_20181106_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='type',
            field=models.CharField(choices=[('Projects', 'Projects'), ('Organizations', 'Organizations')], default='', max_length=30, verbose_name='Section type'),
        ),
    ]
