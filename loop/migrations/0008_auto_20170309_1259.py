# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0007_auto_20170214_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='days_count',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='state',
            name='crop_add',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='state',
            name='helpline_number',
            field=models.CharField(default=b'0', max_length=14),
        ),
        migrations.AlterField(
            model_name='aggregatorincentive',
            name='model_type',
            field=models.IntegerField(choices=[(0, b'Direct'), (1, b'Tax Based'), (2, b'Slab Based'), (3, b'Daily Pay')]),
        ),
    ]
