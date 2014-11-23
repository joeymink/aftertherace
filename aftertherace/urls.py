from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^laps/', include('laps.urls', namespace='laps')),
    url(r'^admin/', include(admin.site.urls)),
)
