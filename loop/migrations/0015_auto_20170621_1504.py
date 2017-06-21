# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0014_auto_20170608_0738'),
    ]

    operations = [
        migrations.CreateModel(
            name='JharkhandIncoming',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('call_id', models.CharField(max_length=100)),
                ('from_number', models.CharField(max_length=20, db_index=True)),
                ('to_number', models.CharField(max_length=20)),
                ('incoming_time', models.DateTimeField()),
                ('user_created', models.ForeignKey(related_name='loop_jharkhandincoming_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_jharkhandincoming_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='jharkhandincoming',
            unique_together=set([('call_id', 'from_number', 'incoming_time')]),
        ),
    ]
