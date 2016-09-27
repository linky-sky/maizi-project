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
from common.forms import RegForm,LoginForm,Basicdata,CommentForm
from PIL import Image
import pytesseract,os,sys
from django.views.generic import TemplateView,RedirectView,ListView,View
from django.contrib.auth.decorators import login_required
from common.views import paging

#其他课程详情页面
def course_kc(request,id):
	othercourse = get_object_or_404(OtherCourses,pk=id)
	#获得章节视频总长
	video_time = OtherCourses.vaidomanager.vm(id)
	try:
		#因为要获得对应视频章节的第一节的id,用于查看视频跳转
		zjid = othercourse.lesson_set.filter().order_by('index')[0].id
	except:
		zjid = 1 #为了获得跳转地址，给出一个1值
	return render(request,'course/cource_kc.html',locals())

#职业课程详情页面
def course_zy(request,seo):
	vocationalcourse = get_object_or_404(VocationalCourses,seo_keyword=seo)
	try:
		#根据用户登录情况来，判断用户是否已报名了该课程
		if request.user.id:
			student = get_object_or_404(UserProfile,pk=request.user.id)
			vo = student.mc_user.filter(course=vocationalcourse.id)
	except:
		vo = None
	return render(request,'course/course_zy.html',locals())


#进行职业课程报名链接  【暂时性的测试】
def baoming(request,id):
	try:
		if request.user.id:
			u_id = request.user.id
			student = get_object_or_404(UserProfile,pk=u_id)
			if student.mc_user.filter(course=id):
				return redirect(request.META['HTTP_REFERER'])
			else:
				student.mc_user.create(user=student,course=id,course_type=2)
	except Exception as e:
		logging.error(e)
	return redirect(request.META['HTTP_REFERER'])


#进行课程的收藏，还没完成，要结合ajax来实现
def shoucang(request,id):
	if request.user.id:
		u_id = request.user.id
		student = get_object_or_404(UserProfile,pk=u_id)
		othercourse = OtherCourses.objects.get(id=id)
		if student.mf_user.filter(course=othercourse):
			s = student.mf_user.filter(course=othercourse)
			s.delete()
			return redirect(request.META['HTTP_REFERER'])
		else:
			student.mf_user.create(user=student,course=othercourse)
			return redirect(request.META['HTTP_REFERER'])


#课程的播放页面
def play(request,id,zjid):
	othercourse = get_object_or_404(OtherCourses,pk=id)
	if request.user.id:
		student = get_object_or_404(UserProfile,id=request.user.id)
		sc = student.mf_user.filter(course=othercourse.id)
	try:
		zid = othercourse.lesson_set.get(pk=zjid)
	except:
		zid = 1 #为了获得跳转地址，给出一个1值,等于没有视频
	#评论
	comment_list = []
	if zid != 1:
		for comment in zid.discuss_set.order_by('id'):
			if comment.parent_id is None:
				comment_list.append(comment)
			for item in comment_list:
				if not hasattr(item,'parent'):
					setattr(item,'parent',[])
				if comment.parent_id == item.id:
					item.parent.append(comment)

		comment_list = paging(request,comment_list,5)

	else:
		pass
	commentform = CommentForm({'article': zjid} if request.user.is_authenticated() else{'article': zjid})
	return render(request,'course/play.html',locals())


#评论回复 ajax
@csrf_exempt
def comment_post(request):
	if request.is_ajax():
		content = request.POST.get('content',None)
		user =  get_object_or_404(UserProfile,id=request.user.id)
		lid = get_object_or_404(Lesson,id=request.POST.get('sid'))
		url = '/uploads/' + str(user.avatar_url)
		if content:
			Discuss.objects.create(content=content,lesson=lid,user=user)
			data = [user.email,content,url]
			return HttpResponse(json.dumps(data))


