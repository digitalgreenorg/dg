# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0009_broadcast_broadcastaudience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcastaudience',
            name='status',
            field=models.IntegerField(default=0, db_index=True, choices=[(0, b'Pending'), (1, b'Done'), (2, b'DND-Failed'), (3, b'Declined')]),
        ),
    ]
