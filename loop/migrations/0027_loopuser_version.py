# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0026_auto_20180109_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='version',
            field=models.CharField(default=b'0', max_length=10, null=True, blank=True),
        ),
    ]
