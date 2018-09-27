# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0021_auto_20180906_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='practice_tag',
            field=models.ForeignKey(blank=True, to='videos.Tag', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='practice',
            unique_together=set([('practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject', 'practice_tag')]),
        ),
    ]
