# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0027_farmer_referral_free_transport_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationsms',
            name='text_local_id',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
