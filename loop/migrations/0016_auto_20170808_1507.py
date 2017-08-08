# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0015_auto_20170621_1504'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jharkhandincoming',
            old_name='incoming_time',
            new_name='start_time',
        ),
        migrations.AddField(
            model_name='jharkhandincoming',
            name='call_type',
            field=models.IntegerField(default=0, choices=[(0, b'Incoming'), (1, b'Outgoing')]),
        ),
        migrations.AddField(
            model_name='jharkhandincoming',
            name='end_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='jharkhandincoming',
            name='is_broadcast',
            field=models.IntegerField(default=0, choices=[(0, b'No'), (1, b'Yes')]),
        ),
        migrations.AddField(
            model_name='jharkhandincoming',
            name='is_picked',
            field=models.IntegerField(default=0, choices=[(0, b'No'), (1, b'Yes')]),
        ),
        migrations.AddField(
            model_name='jharkhandincoming',
            name='name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='jharkhandincoming',
            unique_together=set([('call_id', 'from_number', 'start_time')]),
        ),
    ]
