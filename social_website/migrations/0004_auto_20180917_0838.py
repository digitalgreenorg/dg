# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_website', '0003_auto_20160907_0645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='subtopic',
            new_name='practices',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='topic',
            new_name='tags',
        ),
    ]
