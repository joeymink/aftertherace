from django.conf.urls import patterns, url

from laps import views

urlpatterns = patterns('',
    url(r'^races/$', views.races, name='races'),
)