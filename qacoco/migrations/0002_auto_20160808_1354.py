# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='disseminationquality',
            name='pico',
            field=models.CharField(default=None, max_length=1, choices=[(0, b'Not Working'), (1, b'Working')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='speaker',
            field=models.CharField(default=None, max_length=1, choices=[(0, b'Not Working'), (1, b'Working')]),
            preserve_default=False,
        ),
    ]
