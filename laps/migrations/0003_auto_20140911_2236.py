# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0002_auto_20140911_2235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configurationitem',
            old_name='val',
            new_name='value',
        ),
    ]
