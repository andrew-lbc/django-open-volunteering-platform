# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-28 21:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0040_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Category', verbose_name='category'),
        ),
    ]
