# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_website', '0011_collection_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='tags',
        ),
    ]
