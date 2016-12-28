# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_screening_health_provider_present'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personadoptpractice',
            name='adopt_practice',
            field=models.CharField(max_length=1, null=True, choices=[(1, b'Yes'), (0, b'No'), (2, b'Not Applicable')]),
        ),
        migrations.AlterField(
            model_name='personadoptpractice',
            name='krp_five',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'5'),
        ),
        migrations.AlterField(
            model_name='personadoptpractice',
            name='krp_four',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'4'),
        ),
        migrations.AlterField(
            model_name='personadoptpractice',
            name='krp_one',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'1'),
        ),
        migrations.AlterField(
            model_name='personadoptpractice',
            name='krp_three',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'3'),
        ),
        migrations.AlterField(
            model_name='personadoptpractice',
            name='krp_two',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'2'),
        ),
    ]
