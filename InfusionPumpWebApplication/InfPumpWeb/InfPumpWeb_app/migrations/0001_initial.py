# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-23 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('Doctor', 'Doctor'), ('Patient', 'Patient'), ('Admin', 'Admin')], default='Doctor', max_length=10)),
                ('admin', models.BooleanField(default=False)),
            ],
        ),
    ]
