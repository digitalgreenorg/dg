# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0004_auto_20160810_1140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serverlog',
            old_name='village',
            new_name='district',
        ),
    ]
