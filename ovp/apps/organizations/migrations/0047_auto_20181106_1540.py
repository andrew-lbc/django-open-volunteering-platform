# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-06 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0046_merge_20181105_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.OneToOneField(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.GoogleAddress', verbose_name='address'),
        ),
    ]
