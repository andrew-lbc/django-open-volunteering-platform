# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-18 23:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0083_auto_20190411_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='address',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.GoogleAddress', verbose_name='address'),
        ),
    ]
