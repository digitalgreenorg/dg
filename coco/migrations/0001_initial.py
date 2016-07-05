# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0001_initial'),
        ('programs', '0001_initial'),
        ('geographies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CocoUser',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.IntegerField(null=True, editable=False)),
                ('partner', models.ForeignKey(to='programs.Partner')),
                ('user', models.OneToOneField(related_name='coco_user', to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(related_name='coco_cocouser_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='coco_cocouser_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('videos', models.ManyToManyField(to='videos.Video')),
                ('villages', models.ManyToManyField(to='geographies.Village')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FullDownloadStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServerLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('village', models.IntegerField(null=True)),
                ('action', models.IntegerField()),
                ('entry_table', models.CharField(max_length=100)),
                ('model_id', models.IntegerField(null=True)),
                ('partner', models.IntegerField(null=True)),
                ('user', models.ForeignKey(related_name='serverlog_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
