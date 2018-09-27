# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0024_auto_20180917_0838'),
        ('social_website', '0005_auto_20180917_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='practices',
        ),
        migrations.AddField(
            model_name='collection',
            name='practices',
            field=models.ManyToManyField(to='videos.VideoPractice'),
        ),
    ]
