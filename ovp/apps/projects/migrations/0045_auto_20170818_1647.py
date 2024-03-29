# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-18 16:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0044_merge_20170803_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.VolunteerRole', verbose_name='role'),
        ),
        migrations.AddField(
            model_name='volunteerrole',
            name='applied_count',
            field=models.IntegerField(default=0, verbose_name='Applied count'),
        ),
    ]
