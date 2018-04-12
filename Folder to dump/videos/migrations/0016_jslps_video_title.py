# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0015_jslps_video_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='jslps_video',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
