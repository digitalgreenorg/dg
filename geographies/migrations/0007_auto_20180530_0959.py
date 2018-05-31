# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0006_auto_20180326_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='block_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='district',
            name='district_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='state',
            name='state_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together=set([('block_name', 'district')]),
        ),
        migrations.AlterUniqueTogether(
            name='district',
            unique_together=set([('district_name', 'state')]),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('state_name', 'country')]),
        ),
    ]
