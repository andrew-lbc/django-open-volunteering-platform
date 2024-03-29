# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-11 16:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0012_auto_20170109_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizationinvite',
            options={'verbose_name': 'organization_invite'},
        ),
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.GoogleAddress', verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='causes',
            field=models.ManyToManyField(blank=True, to='core.Cause', verbose_name='causes'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='cover',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='uploads.UploadedImage', verbose_name='cover'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='facebook_page',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='uploads.UploadedImage', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(related_name='organizations_member', to=settings.AUTH_USER_MODEL, verbose_name='members'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.URLField(blank=True, default=None, null=True, verbose_name='Website'),
        ),
    ]
