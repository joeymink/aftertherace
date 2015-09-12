# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0010_auto_20150911_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderchange',
            name='num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
