# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20161231_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='videopractices',
            field=models.ManyToManyField(to='videos.VideoPractice', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='videopractice',
            field=models.ForeignKey(related_name='old_videopractice', blank=True, to='videos.VideoPractice', null=True),
        ),
    ]
