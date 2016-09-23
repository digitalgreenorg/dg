# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('audio_file', models.FileField(upload_to=b'C:\\Users\\Abhishek\\Documents\\dg\\dg\\media\\social_website\\uploadsivrs/')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000, null=True, blank=True)),
                ('audio_status', models.CharField(max_length=20, choices=[(b'1', b'Active'), (b'0', b'InActive')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service', models.CharField(max_length=20, choices=[(b'hello', b'hello'), (b'greeting', b'greeting'), (b'jharkhand_pilot', b'jharkhand_pilot')])),
                ('schedule_call', models.DateTimeField()),
                ('audio_file', models.ForeignKey(to='ivr.Audio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exotel_call_id', models.CharField(max_length=100)),
                ('attributes', models.TextField(max_length=5000)),
                ('state', models.CharField(max_length=100)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IvrSubscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('phone_no', models.CharField(max_length=13)),
                ('subscribed_channels', models.ManyToManyField(to='ivr.Channel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='broadcast',
            name='channels',
            field=models.ManyToManyField(to='ivr.Channel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='audio',
            name='channels',
            field=models.ManyToManyField(to='ivr.Channel'),
            preserve_default=True,
        ),
    ]
