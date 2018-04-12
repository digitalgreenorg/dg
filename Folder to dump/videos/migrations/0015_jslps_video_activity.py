# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0014_auto_20171109_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='jslps_video',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY')]),
        ),
    ]
