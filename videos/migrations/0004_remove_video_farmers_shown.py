# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20160711_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='farmers_shown',
        ),
    ]
