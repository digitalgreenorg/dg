# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0022_auto_20180917_1041'),
        ('social_website', '0003_auto_20160907_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='tags',
            field=models.ManyToManyField(to='videos.Tag', null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='videopractice',
            field=models.ManyToManyField(to='videos.VideoPractice', null=True),
        ),
    ]
