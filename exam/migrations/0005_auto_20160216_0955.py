# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_auto_20160216_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 55, 35, 135914, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 55, 35, 145419, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 55, 35, 141578, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 55, 35, 141511, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progress',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 55, 35, 142984, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 55, 35, 136852, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 55, 35, 131296, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
