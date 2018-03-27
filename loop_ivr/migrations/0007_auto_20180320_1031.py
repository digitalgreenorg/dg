# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0006_auto_20180320_0508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smsstatus',
            old_name='price_info_incoming_id',
            new_name='price_info_incoming',
        ),
    ]
