# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0013_auto_20170517_0805'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jslps_video',
            options={'verbose_name': 'JSLPS Video', 'verbose_name_plural': 'JSLPS Video'},
        ),
    ]
