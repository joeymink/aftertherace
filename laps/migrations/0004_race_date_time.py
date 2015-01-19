# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0003_auto_20141218_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 18, 22, 7, 55, 92891)),
            preserve_default=True,
        ),
    ]
