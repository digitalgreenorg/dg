# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20161210_1243'),
        ('activities', '0005_auto_20161210_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='personadoptpractice',
            name='adopt_practice',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_five',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_four',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_one',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_three',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_two',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='parentcategory',
            field=models.ForeignKey(blank=True, to='videos.ParentCategory', null=True),
        ),
    ]
