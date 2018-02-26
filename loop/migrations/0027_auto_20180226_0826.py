# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0026_auto_20180226_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='qr_code',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
