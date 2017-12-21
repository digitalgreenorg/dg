# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0024_auto_20171221_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loopuser',
            name='registration',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
    ]
