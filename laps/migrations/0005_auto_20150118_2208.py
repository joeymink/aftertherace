# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from datetime import datetime

def set_race_date_time(apps, schema_editor):
    Race = apps.get_model("laps", "Race")
    for race in Race.objects.all():
    	race.date_time = datetime.combine(race.date, datetime.min.time())
    	race.save()

class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0004_race_date_time'),
    ]

    operations = [
	migrations.RunPython(set_race_date_time),
    ]
