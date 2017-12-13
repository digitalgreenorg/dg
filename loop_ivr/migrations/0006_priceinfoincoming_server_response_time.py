# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0005_auto_20171212_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceinfoincoming',
            name='server_response_time',
            field=models.DateTimeField(null=True, verbose_name=b'Time at which server makes API call to textlocal', blank=True),
        ),
    ]
