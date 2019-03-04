from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from . import views

from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^event_log/data/(?P<dataset>.+).json', views.get_dataset),
    url(r'^event_log/$', views.event_log, name='event_log'),
        #login
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # API Urls
    url(r'api/$', views.EventAPIList.as_view()),
    url(r'api/(?P<pk>[0-9]+)/$', views.EventAPIDetail.as_view()),
    url(r'api/device/$', views.DeviceAPIList.as_view()),
    url(r'api/device/(?P<pk>[0-9]+)/$', views.DeviceAPIDetail.as_view()),
    url(r'api/hw/$', views.HwControllerAPIList.as_view()),
    url(r'api/hw/(?P<pk>[0-9]+)/$', views.HwControllerAPIDetail.as_view())
]

#Media file upload
if settings.DEBUG:
  urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
  ]