"""maizi_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from course  import views

#course

urlpatterns = [
    url(r'^baoming/(?P<id>[1-9]+)/',views.baoming,name='baoming'),
    url(r'^shoucang/(?P<id>[1-9]+)/',views.shoucang,name='shoucang'),
    url(r'^comment-post/',views.comment_post,name='comment_post'),
    url(r'^raido/(?P<id>[1-9]+)-(?P<zjid>[1-9]+)/',views.play,name='play'),
    url(r'^(?P<id>[1-9]+)/',views.course_kc,name='course_kc'),
    url(r'^(?P<seo>[A-Za-z]+)/',views.course_zy,name='course_zy'),
]
