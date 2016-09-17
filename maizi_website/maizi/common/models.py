#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/17
@author: huangzhanrong
Common模块View业务处理。
"""



from django.db import models
from datetime import datetime


# Create your models here.


class Ads(models.Model):
	title = models.CharField(max_length=100,verbose_name='广告标题')
	description = models.CharField(max_length=200,verbose_name='广告描述')
	image_url = models.ImageField(upload_to='ad/%Y%m',verbose_name='图片路径')
	callback_url = models.URLField(null=True,blank=True,verbose_name='回调url')
	play = models.BooleanField(default=False,verbose_name='是否播放')
	index = models.IntegerField(verbose_name='排列顺序(从小到大)',default=999)

	class Meta:
		verbose_name = '广告栏'
		verbose_name_plural = verbose_name
		ordering = ['index','id']

	def __str__(self):
		return self.title
