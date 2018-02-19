# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0014_auto_20180202_1008'),
        ('geographies', '0006_auto_20180114_0135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ap_district',
            name='district',
        ),
        migrations.RemoveField(
            model_name='ap_district',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='ap_district',
            name='user_modified',
        ),
        migrations.RemoveField(
            model_name='ap_habitation',
            name='ap_village',
        ),
        migrations.RemoveField(
            model_name='ap_habitation',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='ap_habitation',
            name='user_modified',
        ),
        migrations.RemoveField(
            model_name='ap_mandal',
            name='ap_district',
        ),
        migrations.RemoveField(
            model_name='ap_mandal',
            name='block',
        ),
        migrations.RemoveField(
            model_name='ap_mandal',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='ap_mandal',
            name='user_modified',
        ),
        migrations.RemoveField(
            model_name='ap_village',
            name='ap_mandal',
        ),
        migrations.RemoveField(
            model_name='ap_village',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='ap_village',
            name='user_modified',
        ),
        migrations.RemoveField(
            model_name='ap_village',
            name='village',
        ),
        migrations.DeleteModel(
            name='AP_District',
        ),
        migrations.DeleteModel(
            name='AP_Habitation',
        ),
        migrations.DeleteModel(
            name='AP_Mandal',
        ),
        migrations.DeleteModel(
            name='AP_Village',
        ),
    ]
