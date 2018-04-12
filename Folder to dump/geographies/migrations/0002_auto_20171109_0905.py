# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jslps_block',
            options={'verbose_name': 'JSLPS Block', 'verbose_name_plural': 'JSLPS Block'},
        ),
        migrations.AlterModelOptions(
            name='jslps_district',
            options={'verbose_name': 'JSLPS District', 'verbose_name_plural': 'JSLPS District'},
        ),
        migrations.AlterModelOptions(
            name='jslps_village',
            options={'verbose_name': 'JSLPS Village', 'verbose_name_plural': 'JSLPS Village'},
        ),
    ]
