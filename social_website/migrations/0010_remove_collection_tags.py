# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_website', '0009_auto_20180924_0521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='tags',
        ),
    ]
