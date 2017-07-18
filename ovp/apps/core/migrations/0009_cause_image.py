# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-08 14:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0003_uploadedimage_uuid'),
        ('core', '0008_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='cause',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='uploads.UploadedImage', verbose_name='image'),
        ),
    ]
