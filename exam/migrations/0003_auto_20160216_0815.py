# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_auto_20160216_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 8, 15, 44, 258335, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 8, 15, 44, 265145, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 8, 15, 44, 262912, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 8, 15, 44, 262877, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progress',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 8, 15, 44, 263777, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 8, 15, 44, 259195, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 8, 15, 44, 254825, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
