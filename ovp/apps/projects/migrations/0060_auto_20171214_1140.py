# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0059_auto_20171204_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='categories',
            field=models.ManyToManyField(blank=True, to='projects.Category', verbose_name='categories'),
        ),
    ]
