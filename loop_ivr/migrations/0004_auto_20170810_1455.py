# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0003_subscriber_subscription_subscriptionlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='aggregator',
        ),
        migrations.RemoveField(
            model_name='subscriber',
            name='farmer',
        ),
    ]
