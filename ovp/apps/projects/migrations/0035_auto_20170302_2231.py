# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_project_crowdfunding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='status',
            field=models.CharField(choices=[('applied', 'Applied'), ('unapplied', 'Canceled'), ('confirmed-volunteer', 'Confirmed Volunteer'), ('not-volunteer', 'Not a Volunteer')], default='applied', max_length=30, verbose_name='status'),
        ),
    ]
