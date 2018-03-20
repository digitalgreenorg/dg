# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0026_qrmapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='referral_free_transport_count',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
