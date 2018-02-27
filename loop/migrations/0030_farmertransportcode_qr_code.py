# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0029_auto_20180226_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmertransportcode',
            name='qr_code',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
