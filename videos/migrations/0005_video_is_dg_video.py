# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_remove_video_farmers_shown'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_dg_video',
            field=models.BooleanField(default=False),
        ),
    ]
