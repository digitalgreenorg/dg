# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0010_auto_20171129_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='jslps_person',
            name='group',
            field=models.ForeignKey(blank=True, to='people.JSLPS_Persongroup', null=True),
        ),
    ]
