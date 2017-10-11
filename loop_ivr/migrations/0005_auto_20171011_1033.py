# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0004_auto_20171010_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriptionlog',
            old_name='failed_code',
            new_name='status_code',
        ),
    ]
