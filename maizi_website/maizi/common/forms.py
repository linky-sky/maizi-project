#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/09/20
@author: huangzhanrong
Common模块View业务处理。
"""

from django  import forms
from django.conf import settings
from common.models import UserProfile

class RegForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "请输入邮箱账号", "required": "required","class":"form-control",}),max_length=50,error_messages={"required": "email不能为空",})
	password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入密码", "required": "required","class":"form-control",}),max_length=20,error_messages={"required": "password不能为空",})
	yanzhengma = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "请输入验证码", "required": "required","class":"form-control form-control-captcha fl",}),max_length=10,error_messages={"required": "验证码不能为空",})


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "请输入邮箱账号/手机号","class":"form-control", "required": "required",}), max_length=50,error_messages={"required": "用户或手机不能为空",})
	password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入密码","class":"form-control", "required": "required",}),max_length=20,error_messages={"required": "密码不能为空",})


class Basicdata(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['avatar_url']



class CommentForm(forms.Form):
	comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "form-control","placeholder":"我要评论","required": "required", "cols": "25","rows": "5", "tabindex": "4"}),error_messages={"required":"评论不能为空",})
	article = forms.CharField(widget=forms.HiddenInput())
