# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0031_farmertransportcode_text_local_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmertransportcode',
            name='sms_status',
            field=models.IntegerField(default=0, null=True, blank=True, choices=[(0, b'Fail'), (1, b'Success')]),
        ),
        migrations.AlterField(
            model_name='farmertransportcode',
            name='state',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
