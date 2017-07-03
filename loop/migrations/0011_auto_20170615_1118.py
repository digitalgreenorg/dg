# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0010_auto_20170515_0726'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAssignedDistrict',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('aggregation_switch', models.BooleanField(default=False)),
                ('is_visible', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'default', max_length=100)),
                ('phone_number', models.CharField(default=b'0', max_length=14)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('assigned_districts', models.ManyToManyField(to='loop.District', through='loop.AdminAssignedDistrict', blank=True)),
                ('assigned_loopusers', models.ManyToManyField(to='loop.LoopUser')),
                ('preferred_language', models.ForeignKey(to='loop.Language', null=True)),
                ('user', models.OneToOneField(related_name='admin_user', to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(related_name='loop_adminuser_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_adminuser_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='adminassigneddistrict',
            name='admin_user',
            field=models.ForeignKey(to='loop.AdminUser'),
        ),
        migrations.AddField(
            model_name='adminassigneddistrict',
            name='district',
            field=models.ForeignKey(to='loop.District'),
        ),
        migrations.AddField(
            model_name='adminassigneddistrict',
            name='user_created',
            field=models.ForeignKey(related_name='loop_adminassigneddistrict_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='adminassigneddistrict',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_adminassigneddistrict_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
