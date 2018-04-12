# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_auto_20170508_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='videopractice',
        ),
        migrations.AlterField(
            model_name='video',
            name='videopractices',
            field=models.ManyToManyField(to='videos.VideoPractice', blank=True),
        ),
    ]
