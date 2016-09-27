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
import logging
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.contrib.auth import logout,login,authenticate
from common.forms import RegForm,LoginForm,Basicdata
from PIL import Image
import pytesseract,os,sys
from django.views.generic import TemplateView,RedirectView,ListView,View,DetailView
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger('common.views')

#全局变量
def global_setting(request):
	site_manager = settings.SITE_MANAGER
	site_manager['TITLE'] = "麦子学院 - 专业IT职业在线教育平台|ui设计培训|python培训|php培训|web前端培训"
	site_manager['KEYWORDS'] = "麦子学院，IT职业培训，IT技能培训，IT在线教育，IT在线学习，编程学习，android,ios, php,java,python,html5,cocos2dx"
	site_manager['DESCRIPTION'] = "麦子学院专注IT职业在线教育，提供android开发、ios开发、coocs2d-x、Unity3D、游戏原画、物联网、产品经理、嵌入式、\php等一系列线上IT培训服务，推出在线教育智能化学习系统，保证在线学习效果，每年帮助上万名软件开发学习者成功就业。"
	#广告
	site_manager['ads'] = Ads.objects.filter(play=True)
	#推荐搜索关键词
	site_manager['rsks'] = RecommendedSearchkeywords.objects.filter(display=True)
	#最新课程排名
	site_manager['oc_publishs'] = OtherCourses.objects.filter(is_homeshow=True).order_by('-date_publish')[:8]
	#最多播放排名
	site_manager['oc_clicks'] = OtherCourses.objects.filter(is_homeshow=True).order_by('-click_count')[:8]
	#最具人气排名
	site_manager['oc_students'] = OtherCourses.objects.filter(is_homeshow=True).order_by('-student_count')
	#推荐阅读[技术干货]
	site_manager['articles'] = Articles.objects.filter(reading_type='TC').filter(is_recommend=True)
	#推荐阅读[技术干货]
	site_manager['wikis'] = Articles.objects.filter(reading_type='WK').filter(is_recommend=True)
	#推荐阅读[技术干货]
	site_manager['ins'] = Articles.objects.filter(reading_type='IN').filter(is_recommend=True)
	#友情链接
	site_manager['friendshiplinks'] = FriendshipLinks.objects.filter(display=True)
	#战略合作
	site_manager['strategiccooperations'] = StrategicCooperation.objects.filter(display=True)
	#关注我们
	site_manager['payattentions'] = PayAttention.objects.all()
	#名师风采
	site_manager['userprofiles'] = [up  for up in UserProfile.objects.all() if up.is_teacher()]
	#注册表单
	site_manager['regform'] = RegForm()
	#登录表单
	site_manager['loginform'] = LoginForm()
	return site_manager

#分页功能
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

#主页
class index(TemplateView):
	template_name = 'common/index.html'


#搜索显示课程 ajax
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
			#返回职业课程对应的搜索
			vc_list = VocationalCourses.objects.filter(search_keywords=Keywords.objects.get(\
		name__contains='%s' % (search)))
			#返回其它课程对应的搜索
			oc_list = OtherCourses.objects.filter(search_keywords=Keywords.objects.get(\
		name__contains='%s' % (search)))

			re_list = json.dumps([{"vc":_ajaxdict(request,vc_list)}, {"oc":_ajaxdict(request,oc_list)}])
			#返回的结果例如：'[{'oc':[{'name':'python'}]},{'vc':[{'name':'ios'}]}]'
			return HttpResponse(re_list)
		except:
			return HttpResponse(json.dumps(''))
	else:
		return HttpResponse(json.dumps(''))
	
#教师
def teacher(request,id):
	try:
		#返回id进行教师查找，然后判断是否是教师，要不然再网页上随便输一个ID，则返回结果不实际。
		teacher = get_object_or_404(UserProfile,pk=id)
		if teacher.is_teacher():
			return render(request,'common/teacher.html',locals())
	except Exception as e:
		logging.error(e)
	raise Http404
	

#用户注册 ajax
@csrf_exempt
def do_reg(request):
	if request.is_ajax():
		email = request.POST.get('email')
		password = request.POST.get('password')
		source_url = request.POST.get('source_url')
		yanzhengma = request.POST.get('yanzhengma')
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


#用户注销
def do_logout(request):
	try:
		logout(request)
	except Exception as e:
		logger.error(e)
	return redirect(request.META['HTTP_REFERER'])


#用户登录 ajax
@csrf_exempt
def do_login(request):
	if request.is_ajax():
		# loginform = LoginForm(request.POST)
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


def yanzhengma(request):
	pass


#课程显示列表，通过搜索返回  ajax
def course_lt(request,seo):
	try:
		oc_lt = OtherCourses.objects.filter(name__contains=seo)
		Vc_lt = VocationalCourses.objects.all()
		oc_lts = paging(request,oc_lt,8)
	except Exception as e:
		logging.error(e)
	return render(request,'course/course_lt.html',locals())

