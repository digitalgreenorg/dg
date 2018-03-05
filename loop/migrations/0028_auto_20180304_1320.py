# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0027_referral'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmertransportcode',
            name='msg_type',
            field=models.IntegerField(default=2, choices=[(0, b'Welcome'), (1, b'After-Transport'), (2, b'First-Transport'), (3, b'Referral-Transport')]),
        ),
        migrations.AddField(
            model_name='registrationsms',
            name='msg_type',
            field=models.IntegerField(default=0, choices=[(0, b'Welcome'), (1, b'After-Transport'), (2, b'First-Transport'), (3, b'Referral-Transport')]),
        ),
    ]
