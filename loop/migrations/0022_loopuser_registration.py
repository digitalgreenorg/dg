# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0021_auto_20171218_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='registration',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
