# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-22 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0005_auto_20181017_1947'),
        ('projects', '0065_project_skip_address_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='rating',
            field=models.FloatField(default=None, null=True, verbose_name='Rating'),
        ),
        migrations.AddField(
            model_name='project',
            name='ratings',
            field=models.ManyToManyField(to='ratings.Rating'),
        ),
    ]
