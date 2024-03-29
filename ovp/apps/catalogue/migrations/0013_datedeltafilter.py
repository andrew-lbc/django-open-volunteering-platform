# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ovp.apps.channels.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0007_channelsetting'),
        ('catalogue', '0012_auto_20171003_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateDeltaFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField(default=0, verbose_name='Days')),
                ('weeks', models.IntegerField(default=0, verbose_name='Weeks')),
                ('months', models.IntegerField(default=0, verbose_name='Months')),
                ('years', models.IntegerField(default=0, verbose_name='Years')),
                ('operator', models.CharField(choices=[('exact', 'Exact'), ('gt', 'Greater than'), ('gte', 'Greater than or equal to'), ('lt', 'Lesser than'), ('lte', 'Lesser than or equal to')], default='exact', max_length=30, verbose_name='Operator')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datedeltafilter_channel', to='channels.Channel')),
            ],
            options={
                'abstract': False,
            },
            bases=(ovp.apps.channels.models.mixins.ChannelCreatorMixin, models.Model),
        ),
    ]
