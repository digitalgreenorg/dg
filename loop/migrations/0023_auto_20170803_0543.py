# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0022_auto_20170727_0543'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAssignedLoopUser',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('is_visible', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('district', models.IntegerField(null=True)),
                ('action', models.IntegerField()),
                ('entry_table', models.CharField(max_length=100)),
                ('model_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='language',
            name='notation',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='assigned_loopusers',
            field=models.ManyToManyField(to='loop.LoopUser', through='loop.AdminAssignedLoopUser'),
        ),
        migrations.AddField(
            model_name='adminlog',
            name='admin_user',
            field=models.ForeignKey(to='loop.AdminUser', null=True),
        ),
        migrations.AddField(
            model_name='adminlog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='adminassignedloopuser',
            name='admin_user',
            field=models.ForeignKey(to='loop.AdminUser'),
        ),
        migrations.AddField(
            model_name='adminassignedloopuser',
            name='loop_user',
            field=models.ForeignKey(to='loop.LoopUser'),
        ),
        migrations.AddField(
            model_name='adminassignedloopuser',
            name='user_created',
            field=models.ForeignKey(related_name='loop_adminassignedloopuser_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='adminassignedloopuser',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_adminassignedloopuser_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
