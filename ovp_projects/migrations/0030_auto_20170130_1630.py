# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_projects', '0029_project_minimum_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='minimum_age',
            field=models.IntegerField(default=0, verbose_name='Minimum Age'),
        ),
    ]
