# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        ('people', '0006_person_is_modelfarmer'),
        ('geographies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0004_remove_video_farmers_shown'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdoptionNonNegotiableVerfication',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('adopted', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdoptionVerification',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('verification_date', models.DateField()),
                ('adopt_nonnegotiable', models.ManyToManyField(to='videos.NonNegotiable', through='qacoco.AdoptionNonNegotiableVerfication', blank=True)),
                ('block', models.ForeignKey(to='geographies.Block')),
                ('group', models.ForeignKey(to='people.PersonGroup')),
                ('mediator', models.ForeignKey(to='people.Animator')),
                ('person', models.ForeignKey(to='people.Person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DisseminationQuality',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('equipments_setup_handling', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('context_setting', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('introduce_topic', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('paused_video', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('encouraged_adoption', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('summarized_video', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('subject_knowledge', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('filled_dissemination', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('total_score', models.IntegerField()),
                ('video_grade', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C')])),
                ('remark', models.CharField(max_length=200)),
                ('pico', models.CharField(max_length=1, choices=[(b'0', b'Not Working'), (b'1', b'Working')])),
                ('speaker', models.CharField(max_length=1, choices=[(b'0', b'Not Working'), (b'1', b'Working')])),
                ('block', models.ForeignKey(to='geographies.Block')),
                ('mediator', models.ForeignKey(to='people.Animator')),
            ],
            options={
                'verbose_name_plural': 'Dissemination qualities',
            },
        ),
        migrations.CreateModel(
            name='FullDownloadStats',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user', models.ForeignKey(related_name='qacoco_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QACocoUser',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('blocks', models.ManyToManyField(to='geographies.Block')),
                ('partner', models.ForeignKey(to='programs.Partner')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(related_name='qacoco_qacocouser_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='qacoco_qacocouser_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('videos', models.ManyToManyField(to='videos.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QAReviewerCategory',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(max_length=50)),
                ('user_created', models.ForeignKey(related_name='qacoco_qareviewercategory_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='qacoco_qareviewercategory_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QAReviewerName',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('reviewer_category', models.ForeignKey(to='qacoco.QAReviewerCategory')),
                ('user_created', models.ForeignKey(related_name='qacoco_qareviewername_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='qacoco_qareviewername_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServerLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('block', models.IntegerField(null=True)),
                ('action', models.IntegerField()),
                ('entry_table', models.CharField(max_length=100)),
                ('model_id', models.IntegerField(null=True)),
                ('partner', models.IntegerField(null=True)),
                ('user', models.ForeignKey(related_name='qacocoserverlog_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoQualityReview',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('storystructure', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('framing', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('camera_angles', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('camera_movement', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('light', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('audio_sound', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('continuity', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('interview', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('technical', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('style_guide', models.CharField(blank=True, max_length=1, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3')])),
                ('total_score', models.IntegerField()),
                ('video_grade', models.CharField(max_length=1, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C')])),
                ('approval', models.CharField(max_length=1, choices=[(b'0', b'No'), (b'1', b'Yes')])),
                ('remarks', models.CharField(max_length=200)),
                ('qareviewername', models.ForeignKey(to='qacoco.QAReviewerName')),
                ('user_created', models.ForeignKey(related_name='qacoco_videoqualityreview_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='qacoco_videoqualityreview_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('video', models.ForeignKey(to='videos.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='qareviewername',
            field=models.ForeignKey(to='qacoco.QAReviewerName'),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='user_created',
            field=models.ForeignKey(related_name='qacoco_disseminationquality_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='user_modified',
            field=models.ForeignKey(related_name='qacoco_disseminationquality_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='video',
            field=models.ForeignKey(to='videos.Video'),
        ),
        migrations.AddField(
            model_name='disseminationquality',
            name='village',
            field=models.ForeignKey(to='geographies.Village'),
        ),
        migrations.AddField(
            model_name='adoptionverification',
            name='qareviewername',
            field=models.ForeignKey(to='qacoco.QAReviewerName'),
        ),
        migrations.AddField(
            model_name='adoptionverification',
            name='user_created',
            field=models.ForeignKey(related_name='qacoco_adoptionverification_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='adoptionverification',
            name='user_modified',
            field=models.ForeignKey(related_name='qacoco_adoptionverification_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='adoptionverification',
            name='video',
            field=models.ForeignKey(to='videos.Video'),
        ),
        migrations.AddField(
            model_name='adoptionverification',
            name='village',
            field=models.ForeignKey(to='geographies.Village'),
        ),
        migrations.AddField(
            model_name='adoptionnonnegotiableverfication',
            name='adoptionverification',
            field=models.ForeignKey(to='qacoco.AdoptionVerification'),
        ),
        migrations.AddField(
            model_name='adoptionnonnegotiableverfication',
            name='nonnegotiable',
            field=models.ForeignKey(to='videos.NonNegotiable'),
        ),
        migrations.AddField(
            model_name='adoptionnonnegotiableverfication',
            name='user_created',
            field=models.ForeignKey(related_name='qacoco_adoptionnonnegotiableverfication_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='adoptionnonnegotiableverfication',
            name='user_modified',
            field=models.ForeignKey(related_name='qacoco_adoptionnonnegotiableverfication_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
