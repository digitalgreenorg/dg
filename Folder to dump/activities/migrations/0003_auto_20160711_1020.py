# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20160708_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personadoptpractice',
            name='verification_status',
            field=models.IntegerField(default=0, choices=[(0, b'Not Checked'), (1, b'Approved'), (2, b'Rejected')], validators=[django.core.validators.MaxValueValidator(2)]),
        ),
        migrations.AlterField(
            model_name='personadoptpractice',
            name='verified_by',
            field=models.IntegerField(blank=True, choices=[(0, b'Digital Green'), (1, b'Partner'), (2, b'Third Party')], null=True, validators=[django.core.validators.MaxValueValidator(2)]),
        ),
        migrations.AlterField(
            model_name='screening',
            name='observer',
            field=models.IntegerField(blank=True, choices=[(0, b'Digital Green'), (1, b'Partner'), (2, b'Third Party')], null=True, validators=[django.core.validators.MaxValueValidator(2)]),
        ),
    ]
