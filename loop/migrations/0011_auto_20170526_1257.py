# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0010_auto_20170515_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='phone_digit',
            field=models.CharField(default=10, max_length=2, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='state',
            name='phone_start',
            field=models.CharField(default=789, max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='language',
            name='notation',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='croplanguage',
            name='crop',
            field=models.ForeignKey(related_name='crops', to='loop.Crop'),
        ),
        migrations.CreateModel(
            name='VehicleLanguage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_name', models.CharField(max_length=30)),
                ('language', models.ForeignKey(to='loop.Language', null=True)),
                ('vehicle', models.ForeignKey(related_name='vehicles', to='loop.Vehicle')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
