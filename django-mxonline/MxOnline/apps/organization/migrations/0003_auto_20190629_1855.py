# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-06-29 18:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20190629_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='courses_nums',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='students',
            field=models.IntegerField(default=0, verbose_name='学习人数'),
        ),
    ]
