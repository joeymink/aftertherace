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
	url(r'^registration/', include('registration.backends.default.urls')),

    # Password Reset URLs:
    url(r'^accounts/password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password_reset/mailed/'},
        name="password_reset"),

    url(r'^accounts/password_reset/mailed/$',
        'django.contrib.auth.views.password_reset_done'),

    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/accounts/password_reset/complete/'},
        name='password_reset_confirm',),

    url(r'^accounts/password_reset/complete/$', 
        'django.contrib.auth.views.password_reset_complete'),

)
