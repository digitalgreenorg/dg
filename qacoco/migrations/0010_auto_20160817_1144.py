# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0009_auto_20160817_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disseminationquality',
            name='context_setting',
            field=models.IntegerField(blank=True, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='encouraged_adoption',
            field=models.IntegerField(blank=True, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='equipments_setup_handling',
            field=models.IntegerField(blank=True, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='filled_dissemination',
            field=models.IntegerField(blank=True, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='introduce_topic',
            field=models.IntegerField(blank=True, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='paused_video',
            field=models.IntegerField(blank=True, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='subject_knowledge',
            field=models.IntegerField(blank=True, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='summarized_video',
            field=models.IntegerField(blank=True, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='audio_sound',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='camera_angles',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='camera_movement',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='continuity',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='framing',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='interview',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='light',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='storystructure',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='style_guide',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='technical',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')]),
        ),
    ]
