# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop_ivr', '0002_auto_20170809_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('phone_no', models.CharField(unique=True, max_length=14)),
                ('type_of_subscriber', models.IntegerField(default=2, choices=[(0, b'Farmer'), (1, b'Aggregator'), (2, b'Other')])),
                ('status', models.IntegerField(default=1, choices=[(0, b'Inactive'), (1, b'Active')])),
                ('user_created', models.ForeignKey(related_name='loop_ivr_subscriber_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_ivr_subscriber_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('start_date', models.DateTimeField()),
                ('subscription_code', models.CharField(max_length=150)),
                ('status', models.IntegerField(default=1, choices=[(0, b'Inactive'), (1, b'Active')])),
                ('subscriber', models.ForeignKey(to='loop_ivr.Subscriber')),
                ('user_created', models.ForeignKey(related_name='loop_ivr_subscription_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_ivr_subscription_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionLog',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateTimeField()),
                ('sms_id', models.CharField(max_length=150, null=True, blank=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'Pending'), (1, b'Sent'), (2, b'Failed'), (3, b'Failed-DND')])),
                ('subscription', models.ForeignKey(to='loop_ivr.Subscription')),
                ('user_created', models.ForeignKey(related_name='loop_ivr_subscriptionlog_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_ivr_subscriptionlog_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('subscriber', 'subscription_code')]),
        ),
    ]
