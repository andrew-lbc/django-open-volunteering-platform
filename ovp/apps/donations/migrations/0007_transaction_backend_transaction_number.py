# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-27 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0006_transaction_backend_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='backend_transaction_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
