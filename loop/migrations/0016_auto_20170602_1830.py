# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0015_vehiclelanguage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclelanguage',
            name='time_created',
        ),
        migrations.RemoveField(
            model_name='vehiclelanguage',
            name='time_modified',
        ),
        migrations.RemoveField(
            model_name='vehiclelanguage',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='vehiclelanguage',
            name='user_modified',
        ),
    ]
