# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        ('coco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommCareCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=100)),
                ('is_open', models.BooleanField(default=True)),
                ('person', models.ForeignKey(to='people.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommCareProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=b'True', max_length=100)),
                ('group_name', models.CharField(max_length=100, null=True, blank=True)),
                ('group_id', models.CharField(max_length=100, null=True, blank=True)),
                ('last_updated_time', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommCareUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=40)),
                ('guid', models.CharField(max_length=100)),
                ('coco_user', models.ForeignKey(to='coco.CocoUser')),
                ('mediator', models.ForeignKey(blank=True, to='people.Animator', null=True)),
                ('project', models.ForeignKey(to='dimagi.CommCareProject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='XMLSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_time', models.DateTimeField(editable=False)),
                ('modification_time', models.DateTimeField(auto_now_add=True)),
                ('xml_data', models.TextField()),
                ('error_code', models.IntegerField(null=True)),
                ('error_message', models.TextField(null=True)),
                ('username', models.CharField(max_length=40, blank=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('type', models.CharField(default=b'', max_length=10)),
                ('app_version', models.IntegerField(default=b'0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='commcareuser',
            unique_together=set([('project', 'username')]),
        ),
        migrations.AddField(
            model_name='commcarecase',
            name='project',
            field=models.ForeignKey(to='dimagi.CommCareProject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commcarecase',
            name='user',
            field=models.ForeignKey(to='dimagi.CommCareUser'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='commcarecase',
            unique_together=set([('is_open', 'person', 'project', 'user')]),
        ),
    ]
