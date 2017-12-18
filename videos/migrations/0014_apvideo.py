# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0013_auto_20170517_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='APVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('video_short_name', models.CharField(max_length=40)),
                ('video_short_regionalname', models.CharField(max_length=40)),
                ('bluefrog_practice', models.CharField(max_length=40)),
                ('user_created', models.ForeignKey(related_name='videos_apvideo_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_apvideo_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('video', models.ForeignKey(blank=True, to='videos.Video', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
