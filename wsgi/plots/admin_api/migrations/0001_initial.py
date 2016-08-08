# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-06 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommissionSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=50)),
                ('employee', models.CharField(blank=True, max_length=50)),
                ('agent', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=254)),
                ('slogan', models.CharField(blank=True, max_length=254)),
                ('founded', models.CharField(blank=True, max_length=254)),
                ('email', models.CharField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=254)),
                ('mobile', models.CharField(blank=True, max_length=254)),
                ('website', models.CharField(blank=True, max_length=254)),
                ('alternate_mobile', models.CharField(blank=True, max_length=254)),
                ('address1', models.TextField(blank=True, max_length=254)),
                ('address2', models.TextField(blank=True, max_length=254)),
                ('pin_code', models.CharField(blank=True, max_length=254)),
                ('logo', models.ImageField(null=True, upload_to='logo')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
