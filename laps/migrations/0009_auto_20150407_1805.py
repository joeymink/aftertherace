# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0008_remove_lap_racer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='track',
            field=models.ForeignKey(related_name=b'races', to='laps.Track', null=True),
        ),
    ]
