# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0001_initial'),
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(unique=b'True', max_length=100)),
                ('user_created', models.ForeignKey(related_name='videos_category_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_category_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JSLPS_Video',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vc', models.CharField(max_length=100)),
                ('user_created', models.ForeignKey(related_name='videos_jslps_video_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_jslps_video_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('language_name', models.CharField(unique=b'True', max_length=100)),
                ('user_created', models.ForeignKey(related_name='videos_language_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_language_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NonNegotiable',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('non_negotiable', models.CharField(max_length=500)),
                ('physically_verifiable', models.BooleanField(default=False, db_index=True)),
                ('user_created', models.ForeignKey(related_name='videos_nonnegotiable_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_nonnegotiable_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('practice_name', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Practice',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PracticeSector',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('name', models.CharField(max_length=500)),
                ('user_created', models.ForeignKey(related_name='videos_practicesector_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_practicesector_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PracticeSubject',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('name', models.CharField(max_length=500)),
                ('user_created', models.ForeignKey(related_name='videos_practicesubject_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_practicesubject_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PracticeSubSector',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('name', models.CharField(max_length=500)),
                ('user_created', models.ForeignKey(related_name='videos_practicesubsector_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_practicesubsector_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PracticeSubtopic',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('name', models.CharField(max_length=500)),
                ('user_created', models.ForeignKey(related_name='videos_practicesubtopic_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_practicesubtopic_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PracticeTopic',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('name', models.CharField(max_length=500)),
                ('user_created', models.ForeignKey(related_name='videos_practicetopic_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_practicetopic_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('subcategory_name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='videos.Category')),
                ('user_created', models.ForeignKey(related_name='videos_subcategory_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_subcategory_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'sub categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('title', models.CharField(max_length=200)),
                ('video_type', models.IntegerField(max_length=1, choices=[(1, b'Eligible for Adoption'), (2, b'Not Eligible for adoption')])),
                ('duration', models.TimeField(null=True, blank=True)),
                ('benefit', models.TextField(blank=True)),
                ('production_date', models.DateField()),
                ('approval_date', models.DateField(null=True, blank=True)),
                ('youtubeid', models.CharField(max_length=20, blank=True)),
                ('review_status', models.IntegerField(default=0, max_length=1, choices=[(0, b'Not Reviewed'), (1, b'Reviewed')])),
                ('video_grade', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C')])),
                ('reviewer', models.IntegerField(blank=True, max_length=1, null=True, choices=[(0, b'Digital Green'), (1, b'Partner')])),
                ('category', models.ForeignKey(blank=True, to='videos.Category', null=True)),
                ('farmers_shown', models.ManyToManyField(to='people.Person', null=True, blank=True)),
                ('language', models.ForeignKey(to='videos.Language')),
                ('partner', models.ForeignKey(to='programs.Partner')),
                ('production_team', models.ManyToManyField(to='people.Animator')),
                ('related_practice', models.ForeignKey(blank=True, to='videos.Practice', null=True)),
                ('subcategory', models.ForeignKey(blank=True, to='videos.SubCategory', null=True)),
                ('user_created', models.ForeignKey(related_name='videos_video_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_video_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoPractice',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('videopractice_name', models.CharField(max_length=100)),
                ('subcategory', models.ForeignKey(to='videos.SubCategory')),
                ('user_created', models.ForeignKey(related_name='videos_videopractice_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_videopractice_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='video',
            name='videopractice',
            field=models.ForeignKey(blank=True, to='videos.VideoPractice', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='village',
            field=models.ForeignKey(to='geographies.Village'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together=set([('title', 'production_date', 'language', 'village')]),
        ),
        migrations.AddField(
            model_name='practice',
            name='practice_sector',
            field=models.ForeignKey(default=1, to='videos.PracticeSector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='practice',
            name='practice_subject',
            field=models.ForeignKey(blank=True, to='videos.PracticeSubject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='practice',
            name='practice_subsector',
            field=models.ForeignKey(blank=True, to='videos.PracticeSubSector', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='practice',
            name='practice_subtopic',
            field=models.ForeignKey(blank=True, to='videos.PracticeSubtopic', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='practice',
            name='practice_topic',
            field=models.ForeignKey(blank=True, to='videos.PracticeTopic', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='practice',
            name='user_created',
            field=models.ForeignKey(related_name='videos_practice_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='practice',
            name='user_modified',
            field=models.ForeignKey(related_name='videos_practice_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='practice',
            unique_together=set([('practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject')]),
        ),
        migrations.AddField(
            model_name='nonnegotiable',
            name='video',
            field=models.ForeignKey(to='videos.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jslps_video',
            name='video',
            field=models.ForeignKey(blank=True, to='videos.Video', null=True),
            preserve_default=True,
        ),
    ]
