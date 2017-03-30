# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='full_partner_name',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
