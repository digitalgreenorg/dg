# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0010_personmeetingattendance_direct_beneficiaries_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personmeetingattendance',
            name='category',
        ),
    ]
