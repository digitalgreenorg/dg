# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_auto_20170421_0546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screening',
            name='csp_name',
        ),
        migrations.AddField(
            model_name='screening',
            name='video_type',
            field=models.CharField(blank=True, max_length=20, choices=[(b'1', b'NSA video'), (b'2', b'MIYCN video'), (b'3', b'PLA video'), (b'4', b'PLA meeting')]),
        ),
    ]
