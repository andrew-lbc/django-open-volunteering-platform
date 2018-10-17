# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-17 22:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('ratings', '0004_auto_20181017_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingrequest',
            name='content_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ratingrequest',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
