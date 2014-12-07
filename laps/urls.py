from django.conf.urls import patterns, url

from laps import views

urlpatterns = patterns('',
    url(r'^races/$', views.races, name='races'),
    url(r'^races/(?P<race_id>\d+)/?$', views.race, name='race'),
    url(r'^races/(?P<race_id>\d+)/chart_laps/?$', views.LapsAJAXView.as_view()),
    url(r'^machines/$', views.machines, name='machines'),
    url(r'^machines/(?P<machine_id>\d+)/', views.machine, name='machine'),
    url(r'^tracks/$', views.tracks, name='tracks'),
    url(r'^tracks/(?P<track_id>\d+)/?$', views.track, name='track'),
    url(r'^tracks/(?P<track_id>\d+)/chart_best_avg/?$', views.LapTrendAJAXView.as_view()),
)