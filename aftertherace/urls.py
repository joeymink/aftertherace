from django.conf.urls import patterns, include, url
from django.contrib import admin
import laps

urlpatterns = patterns('',
	url(r'^laps/', include('laps.urls', namespace='laps')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', laps.views.index)
)

import settings
urlpatterns += patterns('',
 (r'^static/', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
 )
