#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/17
@author: huangzhanrong
Common模块View业务处理。
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from common.models import Ads

# Create your views here.

def global_setting(request):
	return blog_manager


def index(request):
	TITLE = "麦子学院 - 专业IT职业在线教育平台|ui设计培训|python培训|php培训|web前端培训"
	KEYWORDS = "麦子学院，IT职业培训，IT技能培训，IT在线教育，IT在线学习，编程学习，android,ios, \
	php,java,python,html5,cocos2dx"
	DESCRIPTION = "麦子学院专注IT职业在线教育，提供android开发、ios开发、coocs2d-x、Unity3D、游戏原画、物联网、产品经理、嵌入式、php等一系列线上IT培训服务，\
	推出在线教育智能化学习系统，保证在线学习效果，每年帮助上万名软件开发学习者成功就业。"
	try:
		ads = Ads.objects.filter(play=True)
	except Exception as e:
		logging.error(e)
	return render(request,'common/index.html',locals())

