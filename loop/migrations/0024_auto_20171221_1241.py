# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0023_auto_20171221_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smslog',
            old_name='test_local_id',
            new_name='text_local_id',
        ),
    ]
