# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0054_auto_20170921_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='categories',
            field=models.ManyToManyField(blank=True, to='projects.Category', verbose_name='categories'),
        ),
    ]
