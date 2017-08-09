# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0019_auto_20170619_0834'),
    ]

    operations = [
    '''
        migrations.CreateModel(
            name='VehicleLanguage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_name', models.CharField(max_length=30)),
            ],
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
        migrations.RemoveField(
            model_name='broadcast',
            name='cluster',
        ),
        migrations.AddField(
            model_name='broadcast',
            name='cluster',
            field=models.ManyToManyField(to='loop.LoopUser'),
        ),
        migrations.AlterField(
            model_name='croplanguage',
            name='crop',
            field=models.ForeignKey(related_name='crops', to='loop.Crop'),
        ),
        migrations.AlterUniqueTogether(
            name='farmer',
            unique_together=set([('phone', 'name', 'village')]),
        ),
        migrations.AlterUniqueTogether(
            name='gaddidar',
            unique_together=set([('gaddidar_phone', 'gaddidar_name', 'mandi')]),
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
        migrations.AddField(
            model_name='gaddidar',
            name='commission',
            field= models.FloatField('Discount',default=1.0))
    '''
    ]
