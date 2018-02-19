# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0005_auto_20180111_0755'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ap_mandal',
            options={'verbose_name': 'AP Block', 'verbose_name_plural': 'AP Block'},
        ),
    ]
