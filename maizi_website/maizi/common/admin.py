#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/17
@author: huangzhanrong
Common模块View业务处理。
"""


from django.contrib import admin
from common.models  import Ads

# Register your models here.

admin.site.register(Ads)