# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-27 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_auto_20190314_1505'),
        ('core', '0033_post_modified_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gallery.Gallery', verbose_name='gallery'),
        ),
    ]
