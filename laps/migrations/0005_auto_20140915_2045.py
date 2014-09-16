# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0004_auto_20140915_2040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configurationattribute',
            old_name='key',
            new_name='attrkey',
        ),
        migrations.RenameField(
            model_name='configurationattribute',
            old_name='value',
            new_name='attrvalue',
        ),
    ]
