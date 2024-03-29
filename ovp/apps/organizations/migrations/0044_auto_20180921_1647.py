# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-21 19:47
from __future__ import unicode_literals

from django.db import migrations, models
import ovp.apps.organizations.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0043_auto_20180904_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='document',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, validators=[ovp.apps.organizations.validators.validate_CNPJ], verbose_name='CNPJ'),
        ),
    ]
