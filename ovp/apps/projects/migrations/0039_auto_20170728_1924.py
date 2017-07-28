# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-28 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0038_auto_20170627_0235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='address',
            field=models.OneToOneField(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.GoogleAddress', verbose_name='address'),
        ),
    ]
