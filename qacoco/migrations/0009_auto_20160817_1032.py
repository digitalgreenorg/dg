# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0008_auto_20160812_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoqualityreview',
            name='approval',
            field=models.CharField(max_length=1, choices=[(b'0', b'No'), (b'1', b'Yes')]),
        ),
    ]
