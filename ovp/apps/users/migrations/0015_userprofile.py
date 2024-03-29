# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 17:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_lead'),
        ('users', '0014_user_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Full name')),
                ('about', models.TextField(blank=True, null=True, verbose_name='About me')),
                ('skills', models.ManyToManyField(to='core.Skill')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
