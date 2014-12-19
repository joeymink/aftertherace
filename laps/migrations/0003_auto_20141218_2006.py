# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def set_num_laps(apps, schema_editor):
    Race = apps.get_model("laps", "Race")
    Lap = apps.get_model("laps", "Lap")
    for race in Race.objects.all():
        q = Lap.objects.filter(race=race).order_by('-num')
        if q.count() > 0:
            race.num_laps = q[0].num
            race.save()

class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0002_race_num_laps'),
    ]

    operations = [
	migrations.RunPython(set_num_laps),
    ]
