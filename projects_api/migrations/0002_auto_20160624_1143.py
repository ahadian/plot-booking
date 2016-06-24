# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_no', models.IntegerField()),
                ('basic_cost', models.CharField(blank=True, max_length=254)),
                ('is_booked', models.BooleanField(default=False)),
                ('is_saled', models.BooleanField(default=False)),
                ('facing', models.CharField(blank=True, max_length=254)),
                ('width', models.CharField(blank=True, max_length=254)),
                ('breadth', models.CharField(blank=True, max_length=254)),
                ('area', models.CharField(blank=True, max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='address',
            field=models.TextField(max_length=254),
        ),
        migrations.AlterField(
            model_name='project',
            name='area',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=254),
        ),
        migrations.AddField(
            model_name='plots',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='projects_api.Project'),
        ),
    ]
