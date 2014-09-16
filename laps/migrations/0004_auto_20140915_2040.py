# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0003_auto_20140911_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurationAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('machine_config', models.ForeignKey(related_query_name=b'attribute', related_name=b'attributes', to='laps.MachineConfiguration')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='configurationitem',
            name='machine_config',
        ),
        migrations.DeleteModel(
            name='ConfigurationItem',
        ),
        migrations.AlterField(
            model_name='machineconfiguration',
            name='machine',
            field=models.ForeignKey(related_name=b'configuration', to='laps.Machine'),
        ),
    ]
