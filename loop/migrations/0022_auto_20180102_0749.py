# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0021_auto_20171208_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsLog',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sms_body', models.CharField(max_length=300, null=True, blank=True)),
                ('text_local_id', models.CharField(max_length=20, null=True, blank=True)),
                ('contact_no', models.CharField(max_length=13, null=True, blank=True)),
                ('person_type', models.IntegerField(default=0, choices=[(0, b'Farmer'), (1, b'Transporter')])),
                ('status', models.IntegerField(default=0, choices=[(0, b'Fail'), (1, b'Success')])),
                ('user_created', models.ForeignKey(related_name='loop_smslog_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_smslog_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='payment_sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='payment_sms_id',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='payment_sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='payment_sms_id',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='registration_sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='farmer',
            name='registration_sms_id',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='percent_farmer_share',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='registration',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='show_farmer_share',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='loopuser',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name=b'Is Active'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name=b'Is Active'),
        ),
    ]
