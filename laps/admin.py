from django.contrib import admin
from laps.models import Race, Racer, Track

admin.site.register(Racer)
admin.site.register(Track)
admin.site.register(Race)
