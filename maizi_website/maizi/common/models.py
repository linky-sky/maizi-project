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
	"""
	广告
	"""
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

class RecommendedSearchkeywords(models.Model):
	"""
	推荐搜索关键词
	"""
	name = models.CharField(max_length=50,verbose_name='推荐搜索关键词')
	index = models.IntegerField(verbose_name='排列顺序(从小到大)',default=999)
	display = models.BooleanField(default=False,verbose_name='是否显示')

	class Meta:
		verbose_name = '推荐搜索关键词'
		verbose_name_plural = verbose_name
		ordering = ['index','id']

	def __str__(self):
		return self.name

class Keywords(models.Model):
	"""
	搜索关键词
	"""
	name = models.CharField(max_length=50,verbose_name='关键词')

	class Meta:
		verbose_name = '关键词'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name

class VocationalCourses(models.Model):
	"""
	职业课程
	"""
	name = models.CharField(max_length=100,verbose_name='职业课程')
	description = models.TextField(verbose_name='课程介绍')
	image = models.ImageField(u'课程封面', upload_to='course/%Y/%m')
	index = models.IntegerField(u'职业课程顺序(从小到大)', default=999)
	search_keywords = models.ManyToManyField(Keywords, verbose_name=u'职业课程搜索关键词')
	date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
	student_count = models.IntegerField(default=0,verbose_name='学习人数')
	favorite_count = models.IntegerField(default=0,verbose_name='收藏人数')

	class Meta:
		verbose_name = '职业课程'
		verbose_name_plural = verbose_name
		ordering = ['-id']

	def __str__(self):
		return self.name

class OtherCourses(models.Model):
	"""
	其他课程
	"""
	name = models.CharField(max_length=100,verbose_name='其他课程')
	description = models.TextField(verbose_name='课程介绍')
	image = models.ImageField(u'课程封面', upload_to='course/%Y/%m')
	index = models.IntegerField(u'职业课程顺序(从小到大)', default=999)
	search_keywords = models.ManyToManyField(Keywords, verbose_name=u'其他课程搜索关键词')
	date_publish = models.DateTimeField(u'发布时间', auto_now_add=True)
	date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
	student_count = models.IntegerField(default=0,verbose_name='学习人数')
	favorite_count = models.IntegerField(default=0,verbose_name='收藏人数')
	click_count = models.IntegerField(default=0,verbose_name='播放次数')
	is_homeshow = models.BooleanField(default=False,verbose_name='是否主页显示')

	class Meta:
		verbose_name = '其他课程'
		verbose_name_plural = verbose_name
		ordering = ['-id']

	def __str__(self):
		return self.name


