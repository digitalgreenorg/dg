# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0024_auto_20180116_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='closing_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='closing_reason',
            field=models.CharField(default=b'', max_length=140, null=True, blank=True),
        ),
    ]
