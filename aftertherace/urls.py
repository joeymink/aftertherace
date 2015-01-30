from django.conf.urls import patterns, include, url
from django.contrib import admin
import laps
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
	url(r'^racers/', include('laps.urls', namespace='laps')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', laps.views.index, name='index'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', laps.views.logout, name='atr_logout'),

)
