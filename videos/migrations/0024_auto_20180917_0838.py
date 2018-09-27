# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0023_auto_20180907_0613'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='library',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='library',
            name='practice_category',
        ),
        migrations.RemoveField(
            model_name='library',
            name='practice_subcategory',
        ),
        migrations.RemoveField(
            model_name='library',
            name='practice_tag',
        ),
        migrations.RemoveField(
            model_name='library',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='library',
            name='user_modified',
        ),
        migrations.DeleteModel(
            name='Library',
        ),
    ]
