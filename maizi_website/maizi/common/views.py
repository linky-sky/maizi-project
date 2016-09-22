#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/17
@author: huangzhanrong
Common模块View业务处理。
"""

from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.conf import settings
from common.models import *
from common.models import Ads,RecommendedSearchkeywords
import logging
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.contrib.auth import logout,login,authenticate
from common.forms import RegForm,LoginForm
from PIL import Image
import pytesseract,os,sys
from django.views.generic import TemplateView,RedirectView,ListView,View
# Create your views here.

def global_setting(request):
	return blog_manager

def paging(request,models,index):
	paginator = Paginator(models,index)
	try:
		page = request.GET.get('page')
		articles_contacts = paginator.page(page)
	except PageNotAnInteger:
		articles_contacts = paginator.page(1)
	except EmptyPage:
		articles_contacts = paginator.page(paginator.num_pages)
	return articles_contacts

def index(request):
	TITLE = "麦子学院 - 专业IT职业在线教育平台|ui设计培训|python培训|php培训|web前端培训"
	KEYWORDS = "麦子学院，IT职业培训，IT技能培训，IT在线教育，IT在线学习，编程学习，android,ios, \
	php,java,python,html5,cocos2dx"
	DESCRIPTION = "麦子学院专注IT职业在线教育，提供android开发、ios开发、coocs2d-x、Unity3D、游戏原画、物联网、产品经理、嵌入式、php等一系列线上IT培训服务，\
	推出在线教育智能化学习系统，保证在线学习效果，每年帮助上万名软件开发学习者成功就业。"

			#广告
	ads = Ads.objects.filter(play=True)
			#推荐搜索关键词
	rsks = RecommendedSearchkeywords.objects.filter(display=True)
			#最新课程排名
	oc_publishs = OtherCourses.objects.filter(is_homeshow=True).order_by('-date_publish')
			#最多播放排名
	oc_clicks = OtherCourses.objects.filter(is_homeshow=True).order_by('-click_count')
			#最具人气排名
	oc_students = OtherCourses.objects.filter(is_homeshow=True).order_by('-student_count')
			#推荐阅读
	articles = Articles.objects.filter(reading_type='TC').filter(is_recommend=True)
			#友情链接
	friendshiplinks = FriendshipLinks.objects.filter(display=True)
			#战略合作
	strategiccooperations = StrategicCooperation.objects.filter(display=True)
			#关注我们
	payattentions = PayAttention.objects.all()
			#名师风采
	userprofiles = [up  for up in UserProfile.objects.all() if up.is_teacher()] 

	oc_publishs_contacts = paging(request,oc_publishs,8)
	oc_clicks_contacts = paging(request,oc_clicks,8)
	oc_students_contacts = paging(request,oc_students,8)

			#注册表单
	regform = RegForm()
	loginform = LoginForm()

	return render(request,'common/index.html',locals())


@csrf_exempt
def seo(request):
	def _ajaxdict(request,model_list):
		re_list = []
		for vc in model_list:
			re_dict = {}
			re_dict['name'] = vc.name
			re_dict['url'] = vc.id
			re_dict['seo_keyword'] = vc.seo_keyword
			re_list.append(re_dict)
		return re_list

	search = request.POST.get('search')
	if search:
		try:
			vc_list = VocationalCourses.objects.filter(search_keywords=Keywords.objects.get(\
		name__contains='%s' % (search)))
			oc_list = OtherCourses.objects.filter(search_keywords=Keywords.objects.get(\
		name__contains='%s' % (search)))

			re_list = json.dumps([{"oc":_ajaxdict(request,vc_list)}, {"vc":_ajaxdict(request,oc_list)}])
			return HttpResponse(re_list)
		except:
			return HttpResponse(json.dumps(''))
	else:
		return HttpResponse(json.dumps(''))
	

def teacher(request,id):
	try:
		teacher = get_object_or_404(UserProfile,pk=id)
		regform = RegForm()
		loginform = LoginForm()
		rsks = RecommendedSearchkeywords.objects.filter(display=True)
	except Exception as e:
		logging.error(e)
	return render(request,'common/teacher.html',locals())


@csrf_exempt
def do_reg(request):
	if request.method == "POST":
		email = request.POST.get('email')
		password = request.POST.get('password')
		yanzhengma = request.POST.get('yanzhengma')
		source_url = request.POST.get('source_url')
		image = Image.open(r'static\test\yzm1.jpeg')
		vcode = pytesseract.image_to_string(image)
		if email:
			if len(password)>8 and len(password)<50:
				if yanzhengma == vcode:
					user = UserProfile.objects.filter(email=email)
					if user:
						return HttpResponse('Email已存在，请重新输入新的邮箱进行注册。')
					else:
						user = UserProfile.objects.create_user(email,password)
						user.save()
						user.backend = 'django.contrib.auth.backends.ModelBackend'
						login(request, user)
						return HttpResponse(source_url)
				else:
					return HttpResponse('验证码错误！')
			else:
				return HttpResponse('密码长度不符合要求！')
		else:
			return HttpResponse('Email不能为空！')


def do_logout(request):
	try:
		logout(request)
	except Exception as e:
		logger.error(e)
	return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def do_login(request):
	try:
		if request.method == "POST":
			loginform = LoginForm(request.POST)
			username = request.POST.get("username")
			password = request.POST.get("password")
			lgsource_url = request.POST.get("lgsource_url")
			user = authenticate(username=username, password=password)
			if user is not None:
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				login(request,user)	
				return HttpResponse(request.POST.get('lgsource_url'))
			else:
				return HttpResponse('账号或者密码有误，请重新输入！')
		else:
			return HttpResponse('')
	except:
		pass


def yanzhengma(request):
	pass


def geren_student(request,id):
	student = get_object_or_404(UserProfile,pk=id)
	regform = RegForm()
	loginform = LoginForm()
	rsks = RecommendedSearchkeywords.objects.filter(display=True)
	return render(request,'users/geren_student.html',locals())


def course_kc(request,id):
	othercourse = get_object_or_404(OtherCourses,pk=id)
	regform = RegForm()
	loginform = LoginForm()
	rsks = RecommendedSearchkeywords.objects.filter(display=True)
	video_time = OtherCourses.vaidomanager.vm(id)
	return render(request,'course/cource_kc.html',locals())


def course_zy(request,id):
	vocationalcourse = get_object_or_404(VocationalCourses,seo_keyword=id)
	regform = RegForm()
	loginform = LoginForm()
	rsks = RecommendedSearchkeywords.objects.filter(display=True)
	return render(request,'course/test.html',locals())


def course_lt(request,id):
	oc_lt = OtherCourses.objects.filter(name__contains=id)
	Vc_lt = VocationalCourses.objects.all()
	oc_lts = paging(request,oc_lt,8)
	regform = RegForm()
	loginform = LoginForm()
	rsks = RecommendedSearchkeywords.objects.filter(display=True)
	return render(request,'course/course_lt.html',locals())

