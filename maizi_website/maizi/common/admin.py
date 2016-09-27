#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/17
@author: huangzhanrong
Common模块View业务处理。
"""


from django.contrib import admin
from common.models import *
from common.models  import Ads,RecommendedSearchkeywords

# Register your models here.

admin.site.register(Ads)
admin.site.register(RecommendedSearchkeywords)
admin.site.register(Keywords)
admin.site.register(VocationalCourses)
admin.site.register(OtherCourses)
admin.site.register(Articles)
admin.site.register(FriendshipLinks)
admin.site.register(StrategicCooperation)
admin.site.register(PayAttention)
admin.site.register(UserProfile)
admin.site.register(Lesson)
admin.site.register(MyCourse)
admin.site.register(LessonResource)
admin.site.register(MyFavorite)
admin.site.register(Discuss)