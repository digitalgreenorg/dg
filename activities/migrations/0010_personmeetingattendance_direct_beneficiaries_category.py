# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_remove_screening_direct_beneficiaries'),
    ]

    operations = [
        migrations.AddField(
            model_name='personmeetingattendance',
            name='direct_beneficiaries_category',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
    ]
