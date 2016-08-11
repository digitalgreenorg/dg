# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_remove_video_farmers_shown'),
        ('qacoco', '0006_auto_20160811_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='qacocouser',
            name='videos',
            field=models.ManyToManyField(to='videos.Video'),
        ),
    ]
