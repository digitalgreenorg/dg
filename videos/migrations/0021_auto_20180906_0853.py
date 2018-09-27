# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0020_auto_20180510_0724'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='practice',
            unique_together=set([('practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject', 'practice_name')]),
        ),
    ]
