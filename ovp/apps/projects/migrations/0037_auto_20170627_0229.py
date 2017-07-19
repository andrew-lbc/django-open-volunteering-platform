# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-27 02:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_merge_20170323_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='address',
            field=models.OneToOneField(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_core.GoogleAddress', verbose_name='address'),
        ),
    ]
