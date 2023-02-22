# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0002_videoqualityreview_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoqualityreview',
            name='ease_of_understanding',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='videoqualityreview',
            name='editing',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='videoqualityreview',
            name='facilitation',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='videoqualityreview',
            name='gender_sensitivity',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='videoqualityreview',
            name='intro_and_importance',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='videoqualityreview',
            name='non_negotiable_pts',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AddField(
            model_name='videoqualityreview',
            name='story_board',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='context_setting',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='encouraged_adoption',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='equipments_setup_handling',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='filled_dissemination',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='introduce_topic',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='paused_video',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='subject_knowledge',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='disseminationquality',
            name='summarized_video',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='audio_sound',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='camera_angles',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='camera_movement',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='continuity',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='framing',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='interview',
            field=models.CharField(default=None, max_length=1, blank=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='light',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='storystructure',
            field=models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='style_guide',
            field=models.CharField(default=None, max_length=1, blank=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='technical',
            field=models.CharField(default=None, max_length=1, blank=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
    ]
