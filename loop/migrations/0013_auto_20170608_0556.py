# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0012_broadcast_cluster'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleLanguage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='language',
            name='notation',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
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
        migrations.AlterField(
            model_name='broadcast',
            name='cluster',
            field=models.ManyToManyField(to='loop.LoopUser'),
        ),
        migrations.AlterField(
            model_name='croplanguage',
            name='crop',
            field=models.ForeignKey(related_name='crops', to='loop.Crop'),
        ),
        migrations.AddField(
            model_name='vehiclelanguage',
            name='language',
            field=models.ForeignKey(to='loop.Language', null=True),
        ),
        migrations.AddField(
            model_name='vehiclelanguage',
            name='vehicle',
            field=models.ForeignKey(related_name='vehicles', to='loop.Vehicle'),
        ),
    ]
