# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-07 11:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='address1',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='company',
            name='address2',
        ),
    ]
