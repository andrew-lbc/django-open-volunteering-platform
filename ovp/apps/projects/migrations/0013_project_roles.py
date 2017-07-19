# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-15 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20161115_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='roles',
            field=models.ManyToManyField(blank=True, to='projects.VolunteerRole', verbose_name='Volunteer Roles'),
        ),
    ]
