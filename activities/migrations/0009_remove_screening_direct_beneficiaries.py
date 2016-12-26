# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0008_auto_20161222_0714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screening',
            name='direct_beneficiaries',
        ),
    ]
