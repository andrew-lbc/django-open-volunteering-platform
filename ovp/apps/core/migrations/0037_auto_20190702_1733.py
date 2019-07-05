# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-02 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
        migrations.AddField(
            model_name='post',
            name='deleted_date',
            field=models.DateTimeField(editable=False, null=True, verbose_name='Deleted date'),
        ),
    ]