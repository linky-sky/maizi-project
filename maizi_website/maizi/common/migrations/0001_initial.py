# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-17 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='广告标题')),
                ('description', models.CharField(max_length=200, verbose_name='广告描述')),
                ('image_url', models.ImageField(upload_to='ad/%Y%m', verbose_name='图片路径')),
                ('callback_url', models.URLField(blank=True, null=True, verbose_name='回调url')),
                ('play', models.BooleanField(default=False, verbose_name='是否播放')),
                ('index', models.IntegerField(verbose_name='排列顺序(从小到大)')),
            ],
            options={
                'ordering': ['index', 'id'],
                'verbose_name': '广告栏',
                'verbose_name_plural': '广告栏',
            },
        ),
    ]
