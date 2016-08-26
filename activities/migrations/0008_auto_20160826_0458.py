# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20160822_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personadoptpractice',
            name='size_land',
            field=models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
