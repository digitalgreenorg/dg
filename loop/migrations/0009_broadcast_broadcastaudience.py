# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0008_auto_20170309_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('audio_url', models.CharField(max_length=130)),
                ('from_number', models.CharField(max_length=20)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('cluster', models.ForeignKey(blank=True, to='loop.LoopUser', null=True)),
                ('user_created', models.ForeignKey(related_name='loop_broadcast_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_broadcast_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BroadcastAudience',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('call_id', models.CharField(max_length=100, null=True, blank=True)),
                ('to_number', models.CharField(max_length=20, db_index=True)),
                ('status', models.IntegerField(default=0, db_index=True, choices=[(0, b'Pending'), (1, b'Done'), (2, b'DND-Failed'), (3, b'Declined')])),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('broadcast', models.ForeignKey(blank=True, to='loop.Broadcast', null=True)),
                ('farmer', models.ForeignKey(blank=True, to='loop.Farmer', null=True)),
                ('user_created', models.ForeignKey(related_name='loop_broadcastaudience_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_broadcastaudience_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
