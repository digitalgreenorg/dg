# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0010_auto_20160817_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disseminationquality',
            name='context_setting',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='encouraged_adoption',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='equipments_setup_handling',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='filled_dissemination',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='introduce_topic',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='paused_video',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='subject_knowledge',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='summarized_video',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
    ]
