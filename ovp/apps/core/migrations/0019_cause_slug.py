# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20170912_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='cause',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, verbose_name='name'),
        ),
    ]
