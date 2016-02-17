# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20160216_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 11, 652539, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 11, 660646, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 11, 657349, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journal',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 11, 657296, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='progress',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 11, 658589, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 11, 653437, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 56, 11, 648517, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
