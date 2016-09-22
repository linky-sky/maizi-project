from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import math

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

