# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-07-14 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[('qdkf', '前端开发'), ('hdkf', '后端开发'), ('qz', '全栈开发')], default='hdkf', max_length=10, verbose_name='课程类别'),
        ),
    ]
