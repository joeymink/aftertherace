# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='num_laps',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
