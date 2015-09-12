# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('laps', '0009_auto_20150407_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiderChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rider_name', models.CharField(max_length=100)),
                ('race', models.ForeignKey(related_name=b'rider_changes', to='laps.Race')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='race',
            name='is_team',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
