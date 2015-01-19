# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0005_auto_20150118_2208'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='race',
            unique_together=set([('name', 'date_time', 'track', 'organization')]),
        ),
        migrations.RemoveField(
            model_name='race',
            name='date',
        ),
        migrations.AlterField(
            model_name='race',
            name='date_time',
            field=models.DateTimeField(),
        ),
    ]
