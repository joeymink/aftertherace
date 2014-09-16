# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0005_auto_20140915_2045'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configurationattribute',
            old_name='attrkey',
            new_name='key',
        ),
        migrations.RenameField(
            model_name='configurationattribute',
            old_name='attrvalue',
            new_name='value',
        ),
    ]
