# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_auto_20170508_0402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='videopractices',
            new_name='videopractice',
        ),
    ]
