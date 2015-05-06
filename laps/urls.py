from django.conf.urls import patterns, url

from laps import views
from laps.views import machines, races

urlpatterns = patterns('',
    url('profile', views.profile, name='profile'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/$', views.racer, name='racer'),

    url(r'^(?P<username>[A-Za-z0-9_]+)/races/$', races.races, name='races'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/races/new/$', races.create_race, name='create_race'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/races/import/$', races.import_race, name='import_race'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/races/(?P<race_id>\d+)/?$', races.race, name='race'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/races/(?P<race_id>\d+)/edit/?$', races.edit_race, name='edit_race'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/races/(?P<race_id>\d+)/edit/laps/?$', races.edit_race_laps, name='edit_race_laps'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/races/(?P<race_id>\d+)/edit/add_config_attr/?$', races.add_config_attr_to_race, name='add_config_attr_to_race'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/races/(?P<race_id>\d+)/chart_laps/?$', views.LapsAJAXView.as_view(), name='chart_laps'),
    
    url(r'^(?P<username>[A-Za-z0-9_]+)/machines/?$', machines.machines, name='machines'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/machines/new/$', machines.create_machine, name='create_machine'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/machines/(?P<machine_id>\d+)/?$', machines.machine, name='machine'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/machines/(?P<machine_id>\d+)/edit/?$', machines.edit_machine, name='edit_machine'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/machines/(?P<machine_id>\d+)/chart_tracks/?$', views.TracksRacedAJAXView.as_view(), name='chart_tracks'),
    
    url(r'^(?P<username>[A-Za-z0-9_]+)/tracks/$', views.tracks, name='tracks'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/tracks/(?P<track_id>\d+)/?$', views.track, name='track'),
    url(r'^(?P<username>[A-Za-z0-9_]+)/tracks/(?P<track_id>\d+)/chart_best_avg/?$', views.LapTrendAJAXView.as_view(), name='chart_best_avg'),
)