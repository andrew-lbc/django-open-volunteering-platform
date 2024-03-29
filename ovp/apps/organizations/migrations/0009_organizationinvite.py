# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-08 15:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0008_auto_20161207_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted_date', models.DateTimeField(blank=True, null=True, verbose_name='Deleted date')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('invitator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_invited', to=settings.AUTH_USER_MODEL)),
                ('invited', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='been_invited', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization')),
            ],
        ),
    ]
