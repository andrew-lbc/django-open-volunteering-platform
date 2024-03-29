# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-06 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0003_uploadedimage_uuid'),
        ('organizations', '0004_organization_causes'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='uploads.UploadedImage'),
        ),
        migrations.AddField(
            model_name='organization',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='facebook_page',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
