# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0016_jslps_adoption_adoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='jslps_screening',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'GOATARY', b'GOATARY')]),
        ),
    ]
