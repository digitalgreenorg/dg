# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0002_auto_20160808_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disseminationquality',
            name='pico',
            field=models.CharField(max_length=1, choices=[(b'0', b'Not Working'), (b'1', b'Working')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='speaker',
            field=models.CharField(max_length=1, choices=[(b'0', b'Not Working'), (b'1', b'Working')]),
        ),
    ]
