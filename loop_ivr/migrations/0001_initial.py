# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0014_auto_20170608_0738'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceInfoIncoming',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('call_id', models.CharField(max_length=100, db_index=True)),
                ('from_number', models.CharField(max_length=20, db_index=True)),
                ('to_number', models.CharField(max_length=20)),
                ('incoming_time', models.DateTimeField()),
                ('info_status', models.IntegerField(default=0, db_index=True, choices=[(0, b'Pending'), (1, b'Done'), (2, b'Wrong Query')])),
                ('query_code', models.CharField(max_length=120, null=True, blank=True)),
                ('price_result', models.TextField(null=True, blank=True)),
                ('return_result_to_app', models.IntegerField(default=1, choices=[(0, b'No'), (1, b'Yes')])),
                ('user_created', models.ForeignKey(related_name='loop_ivr_priceinfoincoming_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_ivr_priceinfoincoming_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PriceInfoLog',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('crop', models.ForeignKey(to='loop.Crop')),
                ('mandi', models.ForeignKey(to='loop.Mandi')),
                ('price_info_incoming', models.ForeignKey(to='loop_ivr.PriceInfoIncoming')),
                ('user_created', models.ForeignKey(related_name='loop_ivr_priceinfolog_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_ivr_priceinfolog_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='priceinfoincoming',
            unique_together=set([('call_id', 'from_number', 'incoming_time')]),
        ),
    ]
