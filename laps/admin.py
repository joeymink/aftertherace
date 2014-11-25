from django.contrib import admin
from laps.models import ConfigurationAttribute, Machine, MachineConfiguration, Race, Racer, Track

admin.site.register(ConfigurationAttribute)
admin.site.register(Machine)
admin.site.register(MachineConfiguration)
admin.site.register(Racer)
admin.site.register(Track)
admin.site.register(Race)
