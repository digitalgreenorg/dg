# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0006_auto_20230926_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoqualityreview',
            name='csa_sensitivity',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
    ]
