# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0018_auto_20170618_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='croplanguage',
            name='measuring_unit',
            field=models.CharField(default=b'kg', max_length=20),
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='is_prime',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='gaddidar',
            name='commission',
        ),
    ]
