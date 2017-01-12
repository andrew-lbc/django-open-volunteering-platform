# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-12 18:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_projects', '0024_auto_20170112_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='max_applies',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='project',
            name='public_project',
            field=models.BooleanField(default=True, verbose_name='Public'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
