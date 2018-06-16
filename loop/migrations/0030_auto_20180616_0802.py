# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0029_registrationsms_call_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissedCall',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sid', models.CharField(default=b'', max_length=80, null=True)),
                ('from_number', models.CharField(max_length=13, null=True, blank=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('user_created', models.ForeignKey(related_name='loop_missedcall_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_missedcall_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='farmertransportcode',
            name='msg_type',
            field=models.IntegerField(default=2, choices=[(0, b'Welcome'), (1, b'After-Transport'), (2, b'First-Transport'), (3, b'Referral-Transport'), (4, b'Already-exist-sms'), (5, b'IVR-Retry')]),
        ),
        migrations.AlterField(
            model_name='registrationsms',
            name='msg_type',
            field=models.IntegerField(default=0, choices=[(0, b'Welcome'), (1, b'After-Transport'), (2, b'First-Transport'), (3, b'Referral-Transport'), (4, b'Already-exist-sms'), (5, b'IVR-Retry')]),
        ),
    ]
