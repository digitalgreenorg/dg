# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    Video = apps.get_model("videos", "Video")
    for video_iterable in Video.objects.all():
        if video_iterable.videopractice_id is not None:
        	video_iterable.videopractices.add(video_iterable.videopractice)


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20170508_0357'),
    ]

    operations = [
    	migrations.RunPython(forward)
    ]
