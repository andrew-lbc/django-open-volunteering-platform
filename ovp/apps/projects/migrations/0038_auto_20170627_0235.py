# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-27 02:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0037_auto_20170627_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='address',
            field=models.OneToOneField(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.GoogleAddress', verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='work',
            name='description',
            field=models.CharField(blank=True, max_length=4000, null=True, verbose_name='Description'),
        ),
    ]
