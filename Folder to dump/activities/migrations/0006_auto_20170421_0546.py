# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20161231_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='screening',
            name='csp_name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='screening',
            name='frontline_worker_present',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'1', b'ANM'), (b'2', b'ASHA'), (b'3', b'AWW')]),
        ),
        migrations.AddField(
            model_name='screening',
            name='type_of_venue',
            field=models.CharField(blank=True, max_length=40, null=True, choices=[(b'1', b'AWC'), (b'2', b'school'), (b'3', b'open space'), (b'4', b'community hall'), (b'5', b'other')]),
        ),
    ]
