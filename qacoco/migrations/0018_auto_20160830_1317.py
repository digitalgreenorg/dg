# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0017_auto_20160830_1259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adoptionverification',
            old_name='nonnegotiable',
            new_name='adopt_nonnegotiable',
        ),
    ]
