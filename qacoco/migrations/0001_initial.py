# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        ('people', '0005_auto_20160708_1744'),
        ('geographies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0004_remove_video_farmers_shown'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdoptionVerification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('verification_date', models.DateField()),
                ('adopted', models.IntegerField(null=True, choices=[(0, b'No'), (1, b'Yes')])),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateField()),
                ('equipments_setup_handling', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('context_setting', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('facilitation', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('subject_knowledge', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('documentation', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('total_score', models.IntegerField()),
                ('video_grade', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C')])),
                ('remark', models.CharField(max_length=200)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user', models.ForeignKey(related_name='qacoco_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QACocoUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('districts', models.ManyToManyField(to='geographies.District')),
                ('partner', models.ForeignKey(to='programs.Partner')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QAReviewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reviewer_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='QAReviewerName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('reviewer_category', models.ForeignKey(to='qacoco.QAReviewer')),
            ],
        ),
        migrations.CreateModel(
            name='ServerLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('village', models.IntegerField(null=True)),
                ('action', models.IntegerField()),
                ('entry_table', models.CharField(max_length=100)),
                ('model_id', models.IntegerField(null=True)),
                ('partner', models.IntegerField(null=True)),
                ('user', models.ForeignKey(related_name='qacocoserverlog_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoContentApproval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('suitable_for', models.IntegerField(choices=[(0, b'Not For Adoption'), (1, b'For Adoption')], validators=[django.core.validators.MaxValueValidator(9)])),
                ('comment', models.CharField(max_length=200)),
                ('qareviewername', models.ForeignKey(to='qacoco.QAReviewerName')),
                ('user_created', models.ForeignKey(related_name='qacoco_videocontentapproval_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='qacoco_videocontentapproval_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('video', models.ForeignKey(to='videos.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoQualityReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('youtubeid', models.CharField(max_length=100)),
                ('storystructure', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('framing', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('camera_angles', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('camera_movement', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('light', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('audio_sound', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('continuity', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('interview', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('technical', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('style_guide', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('total_score', models.IntegerField()),
                ('video_grade', models.CharField(max_length=1, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C')])),
                ('approval', models.IntegerField(choices=[(0, b'No'), (1, b'Yes')])),
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
    ]
