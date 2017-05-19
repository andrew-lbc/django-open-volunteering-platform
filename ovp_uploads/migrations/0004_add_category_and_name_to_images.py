# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-19 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_uploads', '0003_uploadedimage_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageGalery',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('ovp_uploads.uploadedimage',),
        ),
        migrations.AddField(
            model_name='uploadedimage',
            name='category',
            field=models.CharField(blank=True, choices=[('cover', 'Cover'), ('logo', 'Logo')], default=None, max_length=24, null=True, verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='uploadedimage',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Name'),
        ),
    ]
