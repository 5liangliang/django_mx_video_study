# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-07-16 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20190630_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=18, verbose_name='年龄'),
        ),
    ]
