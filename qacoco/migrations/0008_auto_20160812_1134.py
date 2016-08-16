# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0007_qacocouser_videos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disseminationquality',
            old_name='documentation',
            new_name='encouraged_adoption',
        ),
        migrations.RenameField(
            model_name='disseminationquality',
            old_name='facilitation',
            new_name='filled_dissemination',
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='introduce_topic',
            field=models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)]),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='paused_video',
            field=models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)]),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='summarized_video',
            field=models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)]),
        ),
    ]
