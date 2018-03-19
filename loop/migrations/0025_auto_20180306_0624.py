# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0024_auto_20180116_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerQRScan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('timestamp', models.CharField(max_length=20, null=True, blank=True)),
                ('qr_code', models.CharField(default=None, max_length=30)),
                ('action', models.IntegerField(default=0, choices=[(1, b'Pick Up'), (2, b'Payment')])),
                ('user_created', models.ForeignKey(related_name='loop_farmerqrscan_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_farmerqrscan_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FarmerTransportCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('code', models.IntegerField(null=True, blank=True)),
                ('phone', models.CharField(max_length=13, null=True, blank=True)),
                ('dateUsed', models.DateField(null=True, blank=True)),
                ('qr_code', models.CharField(max_length=30, null=True, blank=True)),
                ('sms_status', models.IntegerField(default=0, null=True, blank=True, choices=[(0, b'Fail'), (1, b'Success')])),
                ('state', models.IntegerField(default=0, null=True, blank=True)),
                ('text_local_id', models.CharField(max_length=20, null=True, blank=True)),
                ('msg_type', models.IntegerField(default=2, choices=[(0, b'Welcome'), (1, b'After-Transport'), (2, b'First-Transport'), (3, b'Referral-Transport'), (4, b'Already-exist-sms')])),
                ('user_created', models.ForeignKey(related_name='loop_farmertransportcode_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_farmertransportcode_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('referred_farmer', models.CharField(max_length=13, null=True, blank=True)),
                ('referred_by', models.CharField(max_length=13, null=True, blank=True)),
                ('used', models.BooleanField(default=False)),
                ('user_created', models.ForeignKey(related_name='loop_referral_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_referral_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationSms',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sms_status', models.IntegerField(default=None, null=True, blank=True, choices=[(0, b'Fail'), (1, b'Success')])),
                ('state', models.IntegerField(default=0, null=True, blank=True)),
                ('text_local_id', models.CharField(max_length=20, null=True, blank=True)),
                ('msg_type', models.IntegerField(default=0, choices=[(0, b'Welcome'), (1, b'After-Transport'), (2, b'First-Transport'), (3, b'Referral-Transport'), (4, b'Already-exist-sms')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='farmer',
            name='qr_code',
            field=models.CharField(default=None, max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='referral_free_transport',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='farmer',
            name='referred_by',
            field=models.CharField(default=None, max_length=13, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registrationsms',
            name='farmer',
            field=models.ForeignKey(to='loop.Farmer'),
        ),
        migrations.AddField(
            model_name='registrationsms',
            name='user_created',
            field=models.ForeignKey(related_name='loop_registrationsms_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='registrationsms',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_registrationsms_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
