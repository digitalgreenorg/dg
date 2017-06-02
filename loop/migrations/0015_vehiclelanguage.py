# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0014_auto_20170602_0743'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleLanguage',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_name', models.CharField(max_length=30)),
                ('language', models.ForeignKey(to='loop.Language', null=True)),
                ('user_created', models.ForeignKey(related_name='loop_vehiclelanguage_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_vehiclelanguage_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('vehicle', models.ForeignKey(related_name='vehicles', to='loop.Vehicle')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
