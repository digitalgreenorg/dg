# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0014_auto_20170608_0738'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='farmer',
            unique_together=set([('phone', 'name', 'village')]),
        ),
    ]
