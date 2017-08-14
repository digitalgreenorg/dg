# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0016_auto_20170628_0555'),
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
        migrations.CreateModel(
            name='VehicleLanguage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='adminuser',
            name='village',
            field=models.ForeignKey(default=None, to='loop.Village', null=True),
        ),
        migrations.AddField(
            model_name='croplanguage',
            name='measuring_unit',
            field=models.CharField(default=b'kg', max_length=20),
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='is_prime',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='language',
            name='notation',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='state',
            name='phone_digit',
            field=models.CharField(default=10, max_length=2, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='state',
            name='phone_start',
            field=models.CharField(default=789, max_length=15, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='assigned_loopusers',
            field=models.ManyToManyField(to='loop.LoopUser', through='loop.AdminAssignedLoopUser'),
        ),
        migrations.RemoveField(
            model_name='broadcast',
            name='cluster',
        ),
        migrations.AddField(
            model_name='broadcast',
            name='cluster',
            field=models.ManyToManyField(to='loop.LoopUser'),
        ),
        migrations.AlterField(
            model_name='croplanguage',
            name='crop',
            field=models.ForeignKey(related_name='crops', to='loop.Crop'),
        ),
        migrations.AlterUniqueTogether(
            name='gaddidar',
            unique_together=set([('gaddidar_phone', 'gaddidar_name', 'mandi')]),
        ),
        migrations.AddField(
            model_name='vehiclelanguage',
            name='language',
            field=models.ForeignKey(to='loop.Language', null=True),
        ),
        migrations.AddField(
            model_name='vehiclelanguage',
            name='vehicle',
            field=models.ForeignKey(related_name='vehicles', to='loop.Vehicle'),
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
