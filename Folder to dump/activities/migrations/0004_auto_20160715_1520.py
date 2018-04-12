# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20160711_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personmeetingattendance',
            name='expressed_adoption_video',
        ),
        migrations.RemoveField(
            model_name='personmeetingattendance',
            name='expressed_question',
        ),
        migrations.RemoveField(
            model_name='personmeetingattendance',
            name='interested',
        ),
    ]
