# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0013_auto_20160829_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptionverification',
            name='adopt_nonnegotiable',
            field=models.ManyToManyField(to='videos.NonNegotiable', null=True, through='qacoco.AdoptionNonNegotiableVerfication', blank=True),
        ),
    ]
