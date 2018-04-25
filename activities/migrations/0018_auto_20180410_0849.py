# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0017_ap_adoption_ap_screening'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screening',
            name='type_of_video',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'1', b'NSA video'), (b'2', b'MIYCN video'), (b'3', b'PLA video'), (b'4', b'PLA meeting')]),
        ),
    ]
