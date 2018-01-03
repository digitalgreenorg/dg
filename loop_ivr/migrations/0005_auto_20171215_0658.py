# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0004_auto_20171023_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceinfoincoming',
            name='call_source',
            field=models.IntegerField(default=1, choices=[(1, b'Exotel Call'), (2, b'Textlocal Call'), (3, b'Textlocal SMS')]),
        ),
        migrations.AddField(
            model_name='priceinfoincoming',
            name='server_response_time',
            field=models.DateTimeField(null=True, verbose_name=b'Time at which server makes API call to textlocal', blank=True),
        ),
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='call_id',
            field=models.CharField(max_length=100, verbose_name=b'Call / Message Id', db_index=True),
        ),
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='info_status',
            field=models.IntegerField(default=4, db_index=True, choices=[(0, b'Pending'), (1, b'Done'), (2, b'Wrong Query'), (3, b'No Input'), (4, b'Not Picked/Declined'), (5, b'Call Not Initiated')]),
        ),
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='prev_info_status',
            field=models.IntegerField(default=4, db_index=True, choices=[(0, b'Pending'), (1, b'Done'), (2, b'Wrong Query'), (3, b'No Input'), (4, b'Not Picked/Declined'), (5, b'Call Not Initiated')]),
        ),
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='textlocal_sms_id',
            field=models.TextField(null=True, blank=True),
        ),
    ]
