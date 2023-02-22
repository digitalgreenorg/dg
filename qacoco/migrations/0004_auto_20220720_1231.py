# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0015_auto_20220712_1216'),
        ('qacoco', '0003_auto_20220718_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='disseminationquality',
            name='established_logical_conn',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='group',
            field=models.ForeignKey(default=None, to='people.PersonGroup', null=True),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='maintained_ideal_av_quality',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='maintained_ideal_darkness',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='maintained_ideal_screen_size',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='remote',
            field=models.CharField(max_length=1, null=True, choices=[(b'0', b'Not Working'), (b'1', b'Working')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='context_setting',
            field=models.CharField(default=None, max_length=1, null=True, blank=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
    ]
