# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-12 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_simpleaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='type',
            field=models.CharField(choices=[('company', 'Company'), ('nonprofit', 'Nonprofit')], default='', max_length=10),
        ),
    ]
