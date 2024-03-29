# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-07 19:22
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20180715_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemdocument',
            name='about',
        ),
        migrations.AddField(
            model_name='item',
            name='about',
            field=ckeditor.fields.RichTextField(blank=True, max_length=3000, null=True, verbose_name='About'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Item name'),
        ),
    ]
