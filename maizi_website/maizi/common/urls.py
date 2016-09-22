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
from common  import views
from django.conf import settings
from common.upload  import upload_image

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^seo/',views.seo,name='seo'),
    url(r'^do_reg/',views.do_reg,name='do_reg'),
    url(r'^do_logout/',views.do_logout,name='do_logout'),
    url(r'^do_login/',views.do_login,name='do_login'),
    url(r'^search/course/(?P<id>.+)/',views.course_lt,name='course_lt'),
    url(r'^common/teacher/(?P<id>[1-9]+)/',views.teacher,name='teacher'),
    url(r'^course/(?P<id>[1-9]+)/',views.course_kc,name='course_kc'),
    url(r'^course/(?P<id>[A-Za-z]+)/',views.course_zy,name='course_zy'),
    url(r'^users/student/(?P<id>[1-9]+)/',views.geren_student,name='grs'),
    url(r'^uploads/(?P<path>.*)$','django.views.static.serve',{"document_root":settings.MEDIA_ROOT,}),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
]
