#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/17
@author: huangzhanrong
Common模块View业务处理。
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.conf import settings
from common.models import *
from common.models import Ads,RecommendedSearchkeywords
import logging
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
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
	try:
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

		oc_publishs_contacts = paging(request,oc_publishs,8)
		oc_clicks_contacts = paging(request,oc_clicks,8)
		oc_students_contacts = paging(request,oc_students,8)
	except Exception as e:
		logging.error(e)
	return render(request,'common/index.html',locals())

@csrf_exempt
def seo(request):
	def _ajaxdict(request,model_list):
		re_list = []
		for vc in model_list:
			re_dict = {}
			re_dict['name'] = vc.name
			re_dict['url'] = vc.id
			re_list.append(re_dict)
		return re_list

	search = request.POST.get('search')
	print('-'*100)
	print(search)
	print('-'*100)
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
	
@csrf_exempt
def seooc(request):
	search = request.POST.get('search')
	if search:
		try:
			vc_list = OtherCourses.objects.filter(search_keywords=Keywords.objects.get(\
		name__contains='%s' % (search)))
			re_list = []
			for vc in vc_list:
				re_dict = {}
				re_dict['name'] = vc.name
				re_dict['url'] = vc.id
				re_list.append(re_dict)
			re_list = json.dumps(re_list)
			return HttpResponse(re_list)
		except:
			return HttpResponse(json.dumps(''))
	else:
		return HttpResponse(json.dumps(''))
