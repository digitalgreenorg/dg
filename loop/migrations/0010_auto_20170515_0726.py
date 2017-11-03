# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0009_broadcast_broadcastaudience'),
    ]

    operations = [
        migrations.RenameField(
            model_name='daytransportation',
            old_name='comment',
            new_name='farmer_share_comment',
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='transportation_cost_comment',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
