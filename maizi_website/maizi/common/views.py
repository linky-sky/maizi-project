#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/17
@author: huangzhanrong
Common模块View业务处理。
"""


from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
	return render(request,'common/index.html',locals())

