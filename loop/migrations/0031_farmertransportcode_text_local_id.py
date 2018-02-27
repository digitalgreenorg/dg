# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0030_farmertransportcode_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmertransportcode',
            name='text_local_id',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
