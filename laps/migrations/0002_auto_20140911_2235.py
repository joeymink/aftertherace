# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configurationitem',
            old_name='value',
            new_name='val',
        ),
    ]
