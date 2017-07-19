# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20161025_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (0, 'Sunday')], verbose_name='weekday')),
                ('period', models.PositiveSmallIntegerField(choices=[(0, 'Morning'), (1, 'Afternoon'), (2, 'Evening')], verbose_name='period')),
            ],
            options={
                'verbose_name': 'availability',
            },
        ),
        migrations.AlterField(
            model_name='job',
            name='dates',
            field=models.ManyToManyField(blank=True, to='projects.JobDate'),
        ),
        migrations.AddField(
            model_name='work',
            name='availabilities',
            field=models.ManyToManyField(to='projects.Availability'),
        ),
    ]
