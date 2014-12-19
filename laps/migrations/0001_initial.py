# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurationAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField()),
                ('time', models.DecimalField(max_digits=6, decimal_places=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('machine', models.ForeignKey(related_name=b'configurations', to='laps.Machine')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('organization', models.CharField(max_length=100)),
                ('conditions', models.CharField(max_length=100)),
                ('machine_config', models.ForeignKey(related_name=b'races', blank=True, to='laps.MachineConfiguration', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Racer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first', models.CharField(max_length=100)),
                ('last', models.CharField(max_length=100)),
                ('middle', models.CharField(max_length=100)),
                ('dob', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='race',
            name='track',
            field=models.ForeignKey(related_name=b'races', to='laps.Track'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='race',
            unique_together=set([('name', 'date', 'track', 'organization')]),
        ),
        migrations.AddField(
            model_name='lap',
            name='race',
            field=models.ForeignKey(related_name=b'laps', to='laps.Race'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lap',
            name='racer',
            field=models.ForeignKey(related_name=b'laps', to='laps.Racer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='configurationattribute',
            name='machine_configurations',
            field=models.ManyToManyField(related_name=b'attributes', to='laps.MachineConfiguration'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='configurationattribute',
            unique_together=set([('key', 'value')]),
        ),
    ]
