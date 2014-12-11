from django.conf.urls import patterns, include, url
from django.contrib import admin
import laps
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
	url(r'^laps/', include('laps.urls', namespace='laps')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', laps.views.index),
    url(r'^accounts/login/$', auth_views.login),

)
