# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0004_auto_20161123_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeleteLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('entry_table', models.CharField(max_length=100)),
                ('table_object', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Deleted Logs',
            },
        ),
        migrations.CreateModel(
            name='LogData',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('action', models.IntegerField()),
                ('entry_table', models.CharField(max_length=100)),
                ('model_id', models.IntegerField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='trainer',
            name='training_user',
            field=models.ForeignKey(blank=True, to='training.TrainingUser', null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='facilitator',
            field=models.ForeignKey(related_name='facilitator', blank=True, to='training.Trainer', null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='kind_of_training',
            field=models.BooleanField(default=True, verbose_name=b'New Training'),
        ),
        migrations.AddField(
            model_name='training',
            name='participants_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='training',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='time_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='user_created',
            field=models.ForeignKey(related_name='training_training_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='user_modified',
            field=models.ForeignKey(related_name='training_training_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='trainingType',
            field=models.BooleanField(default=True, verbose_name=b'Without Video'),
        ),
    ]
