# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('image_file', models.CharField(max_length=100)),
                ('sound_file', models.CharField(max_length=100)),
                ('hindi_text', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('image_file', models.CharField(max_length=100)),
                ('sound_file', models.CharField(max_length=100)),
                ('hindi_text', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('image_file', models.CharField(max_length=100)),
                ('sound_file', models.CharField(max_length=100)),
                ('hindi_text', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('image_file', models.CharField(max_length=100)),
                ('sound_file', models.CharField(max_length=100)),
                ('hindi_text', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('table', models.CharField(unique=True, max_length=100)),
                ('title', models.CharField(max_length=1000)),
                ('hindi_text', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website_id', models.CharField(max_length=20)),
                ('image_file', models.CharField(max_length=100)),
                ('sound_file', models.CharField(max_length=100)),
                ('hindi_text', models.CharField(max_length=1000, null=True, blank=True)),
                ('action_type', models.ForeignKey(blank=True, to='videokheti.ActionType', null=True)),
                ('coco_video', models.ForeignKey(to='videos.Video')),
                ('crop', models.ForeignKey(to='videokheti.Crop')),
                ('method', models.ForeignKey(blank=True, to='videokheti.Method', null=True)),
                ('time_year', models.ForeignKey(to='videokheti.TimeYear')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime(2016, 7, 5, 18, 14, 20, 492000))),
                ('text', models.TextField()),
                ('imageURL', models.URLField(max_length=400, null=True, blank=True)),
                ('personName', models.CharField(max_length=300, null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('video', models.ForeignKey(to='videokheti.Video')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='actiontype',
            name='time_year',
            field=models.ForeignKey(to='videokheti.TimeYear'),
            preserve_default=True,
        ),
    ]
