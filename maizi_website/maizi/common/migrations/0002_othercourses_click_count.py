# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-17 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='othercourses',
            name='click_count',
            field=models.IntegerField(default=0, verbose_name='播放次数'),
        ),
    ]