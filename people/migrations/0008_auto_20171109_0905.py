# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_auto_20161114_0611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jslps_animator',
            options={'verbose_name': 'JSLPS Animator', 'verbose_name_plural': 'JSLPS Animator'},
        ),
        migrations.AlterModelOptions(
            name='jslps_animatorassignedvillage',
            options={'verbose_name': 'JSLPS AnimatorAssignedVillage', 'verbose_name_plural': 'JSLPS AnimatorAssignedVillage'},
        ),
        migrations.AlterModelOptions(
            name='jslps_person',
            options={'verbose_name': 'JSLPS Person', 'verbose_name_plural': 'JSLPS Person'},
        ),
        migrations.AlterModelOptions(
            name='jslps_persongroup',
            options={'verbose_name': 'JSLPS Persongroup', 'verbose_name_plural': 'JSLPS Persongroup'},
        ),
    ]
