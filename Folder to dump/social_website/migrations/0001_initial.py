# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('textContent', models.TextField()),
                ('facebookID', models.CharField(max_length=50, null=True, blank=True)),
                ('avatarURL', models.URLField()),
                ('newsFeed', models.BooleanField()),
                ('type', models.PositiveSmallIntegerField()),
                ('titleURL', models.URLField(max_length=400)),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Animator',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('coco_id', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('thumbnailURL', models.URLField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('thumbnailURL', models.URLField()),
                ('state', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=500, blank=True)),
                ('subcategory', models.CharField(max_length=500, blank=True)),
                ('topic', models.CharField(max_length=500, blank=True)),
                ('subtopic', models.CharField(max_length=500, blank=True)),
                ('subject', models.CharField(max_length=500, blank=True)),
                ('likes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('adoptions', models.IntegerField(default=0)),
                ('featured', models.BooleanField(default=False)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime(2016, 7, 5, 18, 14, 20, 354000))),
                ('text', models.TextField()),
                ('isOnline', models.BooleanField()),
                ('animator', models.ForeignKey(blank=True, to='social_website.Animator', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CronTimestamp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('last_time', models.DateTimeField(default=datetime.datetime(2016, 7, 5, 18, 14, 20, 354000))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeaturedCollection',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('collageURL', models.ImageField(help_text=b'Width Should be 642 and Height should be 321', upload_to=b'featured_collection')),
                ('show_on_homepage', models.BooleanField(default=True)),
                ('show_on_language_selection', models.BooleanField(default=True)),
                ('collection', models.ForeignKey(to='social_website.Collection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageSpec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imageURL', models.URLField(max_length=400)),
                ('altString', models.CharField(max_length=200)),
                ('imageLinkURL', models.URLField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('videoNumber', models.IntegerField()),
                ('villageNumber', models.IntegerField()),
                ('screeningNumber', models.IntegerField()),
                ('viewerNumber', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('coco_id', models.CharField(max_length=20, null=True, blank=True)),
                ('name', models.CharField(help_text=b'Partner Name Should not have any spaces or /', unique=True, max_length=100)),
                ('full_name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(max_length=100, blank=True)),
                ('location_image', models.ImageField(help_text=b'Minimum Width Should be 302 and Minimum Height should be 202', null=True, upload_to=b'partner', blank=True)),
                ('joinDate', models.DateField()),
                ('logoURL', models.ImageField(help_text=b'Minimum Width Should be 61 and Minimum Height should be 61', upload_to=b'partner')),
                ('websiteURL', models.URLField(default=b'', max_length=100)),
                ('collection_count', models.PositiveIntegerField(default=0)),
                ('video_count', models.PositiveIntegerField(default=0)),
                ('views', models.BigIntegerField(default=0)),
                ('likes', models.BigIntegerField(default=0)),
                ('adoptions', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('coco_id', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('thumbnailURL', models.URLField(max_length=100)),
                ('partner', models.ForeignKey(to='social_website.Partner')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonVideoRecord',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('personID', models.CharField(max_length=20)),
                ('videoID', models.CharField(max_length=20)),
                ('views', models.PositiveSmallIntegerField(default=0)),
                ('like', models.BooleanField(default=False)),
                ('adopted', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceVideo',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('youtubeID', models.CharField(max_length=50)),
                ('date', models.DateField(default=datetime.datetime(2016, 7, 5, 18, 14, 20, 354000))),
                ('videoTag', models.CharField(default=b'f', max_length=2, choices=[(b'f', b'Film'), (b't', b'Testimonial')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('coco_id', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('thumbnailURL', models.URLField()),
                ('thumbnailURL16by9', models.URLField()),
                ('description', models.TextField(default=b'')),
                ('youtubeID', models.CharField(max_length=20)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('date', models.DateField()),
                ('onlineLikes', models.IntegerField(default=0)),
                ('onlineViews', models.IntegerField(default=0)),
                ('offlineViews', models.IntegerField(default=0)),
                ('adoptions', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=500, blank=True)),
                ('subcategory', models.CharField(max_length=500, blank=True)),
                ('topic', models.CharField(max_length=500, blank=True)),
                ('subtopic', models.CharField(max_length=500, blank=True)),
                ('subject', models.CharField(max_length=500, blank=True)),
                ('language', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=100)),
                ('partner', models.ForeignKey(to='social_website.Partner')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoinCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('collection', models.ForeignKey(to='social_website.Collection')),
                ('video', models.ForeignKey(to='social_website.Video')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(to='social_website.Video')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='milestone',
            name='partner',
            field=models.ForeignKey(to='social_website.Partner', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(to='social_website.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='partner',
            field=models.ForeignKey(to='social_website.Partner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='videos',
            field=models.ManyToManyField(to='social_website.Video', through='social_website.VideoinCollection'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='collection',
            unique_together=set([('title', 'partner', 'state', 'language')]),
        ),
        migrations.AddField(
            model_name='animator',
            name='partner',
            field=models.ForeignKey(to='social_website.Partner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='collection',
            field=models.ForeignKey(blank=True, to='social_website.Collection', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='farmer',
            field=models.ForeignKey(blank=True, to='social_website.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='images',
            field=models.ManyToManyField(to='social_website.ImageSpec', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='partner',
            field=models.ForeignKey(blank=True, to='social_website.Partner', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='video',
            field=models.ForeignKey(blank=True, to='social_website.Video', null=True),
            preserve_default=True,
        ),
    ]
