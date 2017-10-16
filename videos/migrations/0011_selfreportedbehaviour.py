# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0010_auto_20170508_0407'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfReportedBehaviour',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('self_reported_behaviour', models.CharField(max_length=500)),
                ('user_created', models.ForeignKey(related_name='videos_selfreportedbehaviour_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_selfreportedbehaviour_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('video', models.ForeignKey(to='videos.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
