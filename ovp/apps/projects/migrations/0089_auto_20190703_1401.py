# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-03 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0088_auto_20190701_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='documents',
            field=models.ManyToManyField(blank=True, to='uploads.UploadedDocument', verbose_name='documents'),
        ),
        migrations.AlterField(
            model_name='project',
            name='galleries',
            field=models.ManyToManyField(blank=True, to='gallery.Gallery', verbose_name='galleries'),
        ),
        migrations.AlterField(
            model_name='project',
            name='posts',
            field=models.ManyToManyField(blank=True, to='core.Post', verbose_name='posts'),
        ),
    ]
