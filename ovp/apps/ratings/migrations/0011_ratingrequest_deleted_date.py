# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-06 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0010_auto_20181105_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingrequest',
            name='deleted_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
