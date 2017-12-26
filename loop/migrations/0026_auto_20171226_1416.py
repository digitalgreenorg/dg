# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0025_auto_20171221_1408'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smslog',
            old_name='farmer_no',
            new_name='contact_no',
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='payment_sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='payment_sms_id',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='smslog',
            name='person_type',
            field=models.IntegerField(default=0, choices=[(0, b'Farmer'), (1, b'Transporter')]),
        ),
        migrations.AddField(
            model_name='smslog',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Fail'), (1, b'Success')]),
        ),
    ]
