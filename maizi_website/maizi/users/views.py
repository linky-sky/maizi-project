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
from django.views.generic import TemplateView,RedirectView,ListView,View
from django.contrib.auth.decorators import login_required


#登录后台个人资料页面
@login_required
def geren_student(request):
	def _inputform(request,*args,**kwargs):
		for x in args:
			models.update(x=x)


	basicdata = Basicdata()
	if request.user.id:
		u_id = request.user.id
		student = get_object_or_404(UserProfile,pk=u_id)
		vc = [ VocationalCourses.objects.get(id=y.course)  for y in  student.mc_user.all()]

	#个人资料修改POST
	if request.method == 'POST':
		user = Basicdata(request.POST, request.FILES)
		if user.is_valid():
			m = UserProfile.objects.get(pk=u_id)
			if 'default_big.png' in user.cleaned_data['avatar_url']:
				pass
			else:
				m.avatar_url = user.cleaned_data['avatar_url']
			m.username = request.POST['nick_name']
			m.last_name = request.POST['real_name']
			m.email = request.POST['email_name']
			m.ph = request.POST['ph_name']
			m.qq = request.POST['qq']
			m.province = request.POST['province2']
			m.city = request.POST['city2']
			m.save()
			return redirect(request.META['HTTP_REFERER'])

	return render(request,'users/geren_student.html',locals())

#用户后台我的课程页面
@login_required
def my_course(request):
	if request.user.id:
		u_id = request.user.id
		student = get_object_or_404(UserProfile,pk=u_id)
		vc = [ VocationalCourses.objects.get(id=y.course)  for y in  student.mc_user.all()]
	return render(request,'users/my_course.html',locals())


#用户后台我的收藏
@login_required
def my_favorite(request):
	if request.user.id:
		u_id = request.user.id
		student = get_object_or_404(UserProfile,pk=u_id)
		fa = student.mf_user.all()
	return render(request,'users/my_favorite.html',locals())