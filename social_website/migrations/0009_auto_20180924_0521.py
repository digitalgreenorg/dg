# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0024_auto_20180917_0838'),
        ('social_website', '0008_auto_20180920_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='tags',
        ),
        migrations.AddField(
            model_name='collection',
            name='tags',
            field=models.ManyToManyField(to='videos.Tag', db_table=b'videos_Tag', blank=True),
        ),
    ]
