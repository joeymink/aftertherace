# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('laps', '0011_riderchange_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riderchange',
            name='num',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='riderchange',
            name='rider_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='riderchange',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
