# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FBFollowers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fbuser', models.CharField(max_length=64, null=True)),
                ('person', models.CharField(max_length=15, null=True)),
            ],
            options={
                'db_table': 'fb_followers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FBUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fuid', models.CharField(max_length=64)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'fb_user',
            },
            bases=(models.Model,),
        ),
    ]
