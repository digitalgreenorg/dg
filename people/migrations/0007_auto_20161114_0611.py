# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_person_is_modelfarmer'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='animator',
            unique_together=set([('name', 'gender', 'partner', 'district', 'role', 'phone_no')]),
        ),
    ]
