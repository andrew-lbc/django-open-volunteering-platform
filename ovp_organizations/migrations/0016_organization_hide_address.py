# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-13 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_organizations', '0015_merge_20170112_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='hide_address',
            field=models.BooleanField(default=False, verbose_name='Hide address'),
        ),
    ]
