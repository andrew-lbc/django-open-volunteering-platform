# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
