# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_auto_20160216_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 32, 412140, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 32, 420567, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 32, 417071, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 32, 417007, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progress',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 32, 418353, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 32, 413066, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 32, 407668, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
