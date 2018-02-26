# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0025_auto_20180226_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmertransportcode',
            name='sms_status',
            field=models.IntegerField(default=0, choices=[(0, b'Fail'), (1, b'Success')]),
        ),
        migrations.AddField(
            model_name='farmertransportcode',
            name='state',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='registrationsms',
            name='state',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='registrationsms',
            name='sms_status',
            field=models.IntegerField(default=None, choices=[(0, b'Fail'), (1, b'Success')]),
        ),
    ]
