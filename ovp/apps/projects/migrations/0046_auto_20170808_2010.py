# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0045_merge_20170803_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='channels',
            field=models.ManyToManyField(related_name='project_channels', to='channels.Channel'),
        ),
    ]
