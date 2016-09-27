#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/17
@author: huangzhanrong
Common模块View业务处理。
"""



from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
import math

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
	image = models.ImageField(upload_to='course/%Y/%m',verbose_name='课程封面')
	index = models.IntegerField(default=999,verbose_name='职业课程顺序(从小到大)')
	search_keywords = models.ManyToManyField(Keywords, verbose_name='职业课程搜索关键词')
	date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
	student_count = models.IntegerField(default=0,verbose_name='学习人数')
	favorite_count = models.IntegerField(default=0,verbose_name='收藏人数')
	seo_keyword = models.CharField(max_length=200, null=True, blank=True,verbose_name='SEO关键词')

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
	image = models.ImageField(upload_to='course/%Y/%m',verbose_name='课程封面')
	index = models.IntegerField(default=999,verbose_name='职业课程顺序(从小到大)')
	search_keywords = models.ManyToManyField(Keywords, verbose_name='其他课程搜索关键词')
	date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
	date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
	student_count = models.IntegerField(default=0,verbose_name='学习人数')
	favorite_count = models.IntegerField(default=0,verbose_name='收藏人数')
	click_count = models.IntegerField(default=0,verbose_name='播放次数')
	is_homeshow = models.BooleanField(default=False,verbose_name='是否主页显示')
	seo_keyword = models.CharField(max_length=200, null=True, blank=True,verbose_name='SEO关键词')

	class VaidoManager(models.Manager):
		def vm(self,id):
			l = Lesson.objects.filter(course_id=id)
			t = math.ceil(sum([ x.video_length for x in l])/3600)
			return t

	class Meta:
		verbose_name = '其他课程'
		verbose_name_plural = verbose_name
		ordering = ['-id']

	def __str__(self):
		return self.name

	objects = models.Manager()
	vaidomanager = VaidoManager()



class Articles(models.Model):
	"""
	文章
	"""
	EG = 'EG'
	TC = 'TC'
	WK = 'WK'
	IN = 'IN'
	AV = 'AV'
	READING_TYPES = (
		(EG,'就业指导'),
		(TC,'技术干货'),
		(WK,'麦子百科'),
		(IN,'行业资讯'),
		(AV, '官方活动'),
	)

	reading_type = models.CharField(max_length=10,choices=READING_TYPES,default=AV,verbose_name='文章分类')
	title = models.CharField(max_length=100,verbose_name='文章标题')
	desc = models.CharField(max_length=100, verbose_name='文章描述')
	content = models.TextField(verbose_name='文章内容')
	click_count = models.IntegerField(default=0, verbose_name='浏览次数')
	is_recommend = models.BooleanField(default=False, verbose_name='是否推荐阅读至首页')
	date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
	index = models.IntegerField(default=999,verbose_name='文章排列顺序(从小到大)')

	class Meta:
		verbose_name = '文章'
		verbose_name_plural = verbose_name
		ordering = ['index','id']

	def __str__(self):
		return self.title



class FriendshipLinks(models.Model):
	"""
	友情链接
	"""
	name = models.CharField(max_length=20,verbose_name='友情链接名称')
	callback_url = models.URLField(verbose_name='url链接地址')
	date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
	display = models.BooleanField(default=True,verbose_name='是否主页显示')
	index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

	class Meta:
		verbose_name = '友情链接'
		verbose_name_plural = verbose_name
		ordering = ['index','id']

	def __str__(self):
		return self.name


class StrategicCooperation(models.Model):
	"""
	战略合作
	"""
	name = models.CharField(max_length=20,verbose_name='战略合作名称')
	callback_url = models.URLField(verbose_name='链接地址')
	image_url = models.ImageField(upload_to='cooperation/%Y/%m',verbose_name='图片')
	index = models.IntegerField(default=999,verbose_name='按顺序排列(从小到大')
	display = models.BooleanField(default=True,verbose_name='是否主页显示')

	class Meta:
		verbose_name = '战略合作'
		verbose_name_plural = verbose_name
		ordering = ['index','id']

	def __str__(self):
		return self.name

class PayAttention(models.Model):
	"""
	关注我们
	"""
	name = models.CharField(max_length=20,verbose_name='名称')
	class_name = models.CharField(max_length=20,verbose_name='类名称')
	callback_url = models.URLField(verbose_name='链接地址')
	index = models.IntegerField(default=999,verbose_name='按顺序排列(从小到大')

	class Meta:
		verbose_name = '关注我们'
		verbose_name_plural = verbose_name
		ordering = ['index','id']

	def __str__(self):
		return self.name

class UserProfileManager(BaseUserManager):
	'''
	自定义用户管理器
	'''
	def _create_user(self, username, email, password,is_staff, is_superuser, **extra_fields):
		'''
		根据用户名和密码创建一个用户
		'''
		now = datetime.now()
		if not email:
			raise ValueError('Email必须填写')
		user = self.model(username=username,email=email,is_staff=is_staff, is_active=True,is_superuser=is_superuser, last_login=now,date_joined=now, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		return self._create_user(email, email, password, False, False,**extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, email, password, True, True,**extra_fields)

class UserProfile(AbstractBaseUser,PermissionsMixin):
	"""
	用户
	"""
	username = models.CharField(max_length=30,verbose_name='昵称',unique=True)
	first_name = models.CharField(max_length=30,verbose_name='姓氏',blank=True)
	last_name = models.CharField(max_length=30,verbose_name='名字',blank=True)
	email = models.EmailField(verbose_name='email',unique=True,null=True,blank=True)
	is_staff = models.BooleanField(default=False,help_text='是否可以登录到后台管理站点',verbose_name='职员状态')
	is_active = models.BooleanField(default=True,help_text='指明用户是否被认为活跃的。以反选代替删除帐号',verbose_name='有效状态')
	date_joined = models.DateTimeField(auto_now_add=True,verbose_name='创建日期')
	avatar_url = models.ImageField(upload_to='avatar/%Y/%m',default='avatar/default_big.png',max_length=200,blank=True,null=True,verbose_name='头像220x220')
	avatar_middle_thumbnall = models.ImageField(upload_to='avatar/%Y/%m',default='avatar/default_middle.png',max_length=200,blank=True,null=True,verbose_name='头像104x104')
	avatar_small_thumbnall = models.ImageField(upload_to='avatar/%Y/%m',default='avatar/default_samll.png',max_length=200,blank=True,null=True,verbose_name='头像70x70')
	avatar_alt = models.CharField(max_length=100,blank=True,null=True,verbose_name='头像ALT说明')
	qq = models.CharField(max_length=20,blank=True,null=True,verbose_name='QQ号码')
	mobile = models.CharField(max_length=11,blank=True,null=True,unique=True)
	valid_email = models.SmallIntegerField(default=0,choices=((0,'否'),(1,'是'),),verbose_name='是否验证邮箱')
	company_name = models.CharField(max_length=150,blank=True,null=True,verbose_name='公司名')
	position = models.CharField(max_length=100,blank=True,null=True,verbose_name='职位名')
	description = models.TextField(blank=True,null=True,verbose_name='个人介绍')
	city = models.CharField(max_length=30,null=True,blank=True,verbose_name='城市')
	province = models.CharField(max_length=30,null=True,blank=True,verbose_name='省份')
	index = models.IntegerField(default=999,verbose_name='按顺序排列(从小到大)')

	objects = UserProfileManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = '用户'
		verbose_name_plural = verbose_name

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name,self.last_name)
		return full_name

	def get_short_name(self):
		return self.first_name

	def is_teacher(self):
		if self.groups.filter(name='老师').count() > 0:
			return True
		return False

	def is_student(self):
		if self.groups.filter(name='学生').count() > 0:
			return True
		return False

	def __str__(self):
		return self.username

class Lesson(models.Model):
	'''
	视频章节
	'''
	name = models.CharField(max_length=50,verbose_name='章节名称')
	video_url = models.CharField(max_length=200,verbose_name='视频资源URL')
	video_length = models.IntegerField(verbose_name='视频长度（秒）')
	play_count = models.IntegerField(default=0,verbose_name='播放次数')
	share_count = models.IntegerField(default=0,verbose_name='分享次数')
	index = models.IntegerField(default=999,verbose_name='章节顺序(从小到大)')
	course = models.ForeignKey(OtherCourses, verbose_name='课程')

	class Meta:
		verbose_name = '视频章节'
		verbose_name_plural = verbose_name
		ordering = ['index', 'id']

	def __str__(self):
		return self.name

class LessonResource(models.Model):
	'''
	章节资源
	'''
	name = models.CharField(max_length=50,verbose_name='章节资源名称')
	download_url = models.FileField(upload_to='lesson/%Y/%m',verbose_name='下载地址')
	download_count = models.IntegerField(default=0,verbose_name='下载次数')
	lesson = models.ForeignKey(Lesson, verbose_name='章节')
	class Meta:
		verbose_name = '章节资源'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

class MyCourse(models.Model):
	'''
	我的课程
	'''
	user = models.ForeignKey(UserProfile, related_name='mc_user', verbose_name='用户')
	course = models.CharField(max_length=10,verbose_name='课程ID')
	# course = models.ForeignKey(VocationalCourses,verbose_name='课程')
	course_type = models.SmallIntegerField(choices=((1, '其他'), (2, '职业课程'),),verbose_name='课程类型')
	index = models.IntegerField(default=999,verbose_name='课程显示顺序(从小到大)')
	date_add = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

	class Meta:
		verbose_name = '我的课程'
		verbose_name_plural = verbose_name

	def __str__(self):
		return str(self.id)


class MyFavorite(models.Model):
	'''
	我的收藏
	'''
	user = models.ForeignKey(UserProfile, related_name='mf_user', verbose_name='用户')
	course = models.ForeignKey(OtherCourses, verbose_name='课程')
	date_favorite = models.DateTimeField(auto_now_add=True,verbose_name='收藏时间')

	class Meta:
		verbose_name = '我的收藏'
		verbose_name_plural = verbose_name
		unique_together = (('user', 'course'),)

	def __str__(self):
		return str(self.id)
		
class Discuss(models.Model):
	'''
	章节讨论
	'''
	content = models.TextField(verbose_name='讨论内容')
	parent_id = models.IntegerField(blank=True, null=True,verbose_name='父讨论ID')
	date_publish = models.DateTimeField(auto_now_add = True,verbose_name='发布时间')
	lesson = models.ForeignKey(Lesson, verbose_name='章节')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')

	class Meta:
		verbose_name = '课程讨论'
		verbose_name_plural = verbose_name

	def __str__(self):
		return str(self.id)



