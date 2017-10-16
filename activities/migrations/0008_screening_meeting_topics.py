# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20170424_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='screening',
            name='meeting_topics',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[(b'1', b'Introduction and understanding social inequities'), (b'2', b'Understanding underlying causes of under nutrition'), (b'3', b'Identifying problems that affect nutrition conditions during the 1000-day '), (b'4', b'Prioritizing problems '), (b'5', b'Understanding the causes and effects '), (b'6', b'Understanding barriers and opportunities'), (b'7', b'Accountability and sharing of Responsibilities'), (b'8', b'Planning and sharing of responsibilities for Village interface Meeting ')]),
        ),
    ]
