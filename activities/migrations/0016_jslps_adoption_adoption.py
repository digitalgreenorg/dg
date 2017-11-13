# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0015_auto_20171109_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='jslps_adoption',
            name='adoption',
            field=models.ForeignKey(blank=True, to='activities.PersonAdoptPractice', null=True),
        ),
    ]
