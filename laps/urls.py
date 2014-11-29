from django.conf.urls import patterns, url

from laps import views

urlpatterns = patterns('',
    url(r'^races/$', views.races, name='races'),
    url(r'^races/(?P<race_id>\d+)/', views.race, name='race'),
    url(r'^machines/$', views.machines, name='machines'),
    url(r'^machines/(?P<machine_id>\d+)/', views.machine, name='machine'),
)