# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0023_language_countries'),
        ('qacoco', '0005_auto_20220721_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='disseminationquality',
            name='videoes_screened',
            field=models.ManyToManyField(related_name='dissemination_observations', to='videos.Video'),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='video',
            field=models.ForeignKey(blank=True, to='videos.Video', null=True),
        ),
    ]
