# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0010_auto_20170515_0726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcast',
            name='cluster',
        ),
    ]