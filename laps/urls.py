from django.conf.urls import patterns, url

from laps import views

urlpatterns = patterns('',
    url('profile', views.profile, name='profile'),
    url(r'^(?P<username>[a-z0-9_]+)/$', views.racer, name='racer'),

    url(r'^(?P<username>[a-z0-9_]+)/races/$', views.races, name='races'),
    url(r'^(?P<username>[a-z0-9_]+)/races/new/$', views.create_race, name='create_race'),
    url(r'^(?P<username>[a-z0-9_]+)/races/(?P<race_id>\d+)/?$', views.race, name='race'),
    url(r'^(?P<username>[a-z0-9_]+)/races/(?P<race_id>\d+)/edit/?$', views.edit_race, name='edit_race'),
    url(r'^(?P<username>[a-z0-9_]+)/races/(?P<race_id>\d+)/edit/laps/?$', views.edit_race_laps, name='edit_race_laps'),
    url(r'^(?P<username>[a-z0-9_]+)/races/(?P<race_id>\d+)/edit/add_config_attr/?$', views.add_config_attr_to_race, name='add_config_attr_to_race'),
    url(r'^(?P<username>[a-z0-9_]+)/races/(?P<race_id>\d+)/chart_laps/?$', views.LapsAJAXView.as_view(), name='chart_laps'),
    
    url(r'^(?P<username>[a-z0-9_]+)/machines/?$', views.machines, name='machines'),
    url(r'^(?P<username>[a-z0-9_]+)/machines/(?P<machine_id>\d+)/?$', views.machine, name='machine'),
    url(r'^(?P<username>[a-z0-9_]+)/machines/(?P<machine_id>\d+)/chart_tracks/?$', views.TracksRacedAJAXView.as_view(), name='chart_tracks'),
    
    url(r'^(?P<username>[a-z0-9_]+)/tracks/$', views.tracks, name='tracks'),
    url(r'^(?P<username>[a-z0-9_]+)/tracks/(?P<track_id>\d+)/?$', views.track, name='track'),
    url(r'^(?P<username>[a-z0-9_]+)/tracks/(?P<track_id>\d+)/chart_best_avg/?$', views.LapTrendAJAXView.as_view(), name='chart_best_avg'),
)