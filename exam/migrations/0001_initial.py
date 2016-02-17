# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(verbose_name='email address', unique=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], default='MALE', max_length=6)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('country', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('institution', models.CharField(blank=True, max_length=500)),
                ('position', models.CharField(blank=True, max_length=500)),
                ('registration_date', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 35, 627089, tzinfo=utc))),
                ('rating', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(related_query_name='user', blank=True, to='auth.Group', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', blank=True, to='auth.Permission', verbose_name='user permissions', help_text='Specific permissions for this user.', related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('date_and_time', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 35, 629790, tzinfo=utc))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(blank=True, null=True, max_length=500)),
                ('email', models.EmailField(blank=True, null=True, max_length=75)),
                ('feedback', models.TextField()),
                ('date_and_time', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 35, 636509, tzinfo=utc))),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 35, 633147, tzinfo=utc))),
                ('end_date', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 35, 633198, tzinfo=utc))),
                ('number_of_questions', models.IntegerField()),
                ('number_of_correct_answers', models.IntegerField(default=0)),
                ('result', models.IntegerField(default=0)),
                ('report', models.BinaryField()),
                ('test_object', models.BinaryField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 35, 634533, tzinfo=utc))),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('result_list', models.BinaryField(blank=True, null=True)),
                ('current_result', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True)),
                ('test', models.BinaryField(blank=True)),
                ('date_and_time', models.DateTimeField(default=datetime.datetime(2016, 2, 16, 7, 20, 35, 630410, tzinfo=utc))),
                ('rating', models.IntegerField(default=0)),
                ('is_public', models.BooleanField(default=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(to='exam.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='test_images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnregisteredUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(blank=True, null=True, max_length=75)),
                ('first_name', models.TextField()),
                ('middle_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='progress',
            name='test',
            field=models.ForeignKey(to='exam.Test'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='progress',
            name='unregistered_user',
            field=models.ForeignKey(blank=True, null=True, to='exam.UnregisteredUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='progress',
            name='user',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journal',
            name='test',
            field=models.ForeignKey(to='exam.Test'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journal',
            name='unregistered_user',
            field=models.ForeignKey(blank=True, null=True, to='exam.UnregisteredUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journal',
            name='user',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
