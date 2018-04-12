# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('pub_date', models.DateField(verbose_name=b'Date Published on')),
                ('source', models.CharField(max_length=300)),
                ('location', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('link', models.URLField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(default=5)),
                ('comments', models.CharField(max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateField(default=datetime.datetime(2016, 7, 5, 18, 14, 20, 354000))),
                ('time', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
            options={
                'verbose_name_plural': 'Feedback',
            },
            bases=(models.Model,),
        ),
    ]
