# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-02 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_post_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='title'),
        ),
    ]
