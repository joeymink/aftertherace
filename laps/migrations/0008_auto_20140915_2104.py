# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0007_auto_20140915_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configurationattribute',
            name='machine_config',
            field=models.ForeignKey(related_name=b'attributes', to='laps.MachineConfiguration'),
        ),
        migrations.AlterField(
            model_name='machineconfiguration',
            name='machine',
            field=models.ForeignKey(related_name=b'configurations', to='laps.Machine'),
        ),
    ]
