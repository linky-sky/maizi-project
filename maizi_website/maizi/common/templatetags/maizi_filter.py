from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import math
from django.utils import timezone

register = template.Library()


@register.filter()
def time(value):
	fen = math.floor(value/60)
	miao = value - fen *60
	if 10 > fen :
		fen = '0' + str(fen)
	if 10 > miao:
		miao = '0' + str(miao)
	return str(fen) + ':' +str(miao)


@register.filter(name="filter_time")
def filter_time(values):
	if timezone.now() > values:
		cha =  timezone.now() - values
		if cha.days:
			if int(cha.days/7/4/12):
				time = int(cha.days/7/4/12)
				return '%s年前发布' % str(time)
			elif int(cha.days/7/4):
				time = int(cha.days/7/4)
				return '%s月前发布' % str(time)
			elif int(cha.days/7):
				time = int(cha.days/7)
				return '%s周时前发布' % str(time)
			else:
				return '%s天前发布' % str(cha.days)
		elif cha.seconds:
			if int(cha.seconds/60) > 60:
				time = int(cha.seconds/60/60)
				return '%s小时前发布' % str(time)
			else:
				time = int(cha.seconds/60)
				return '%s分钟前发布' % str(time)
		else:
			pass