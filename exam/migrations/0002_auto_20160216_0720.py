# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 38, 952146, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 38, 960661, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 38, 957062, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 38, 957013, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progress',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 38, 958277, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 38, 953054, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 38, 948109, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
