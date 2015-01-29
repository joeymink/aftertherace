# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0007_auto_20150126_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lap',
            name='racer',
        ),
    ]
