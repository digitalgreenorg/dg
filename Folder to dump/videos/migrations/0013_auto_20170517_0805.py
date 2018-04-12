# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selfreportedbehaviour',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='selfreportedbehaviour',
            name='user_modified',
        ),
        migrations.RemoveField(
            model_name='selfreportedbehaviour',
            name='video',
        ),
        migrations.AddField(
            model_name='video',
            name='self_reported_behaviour1',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='self_reported_behaviour2',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='SelfReportedBehaviour',
        ),
    ]
