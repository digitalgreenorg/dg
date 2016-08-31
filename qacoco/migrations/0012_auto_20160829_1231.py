# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0004_remove_video_farmers_shown'),
        ('qacoco', '0011_auto_20160817_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdoptionNonNegotiableVerfication',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('adopted', models.CharField(blank=True, max_length=1, null=True, choices=[(b'0', b'No'), (b'1', b'Yes')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='adoptionverification',
            name='adopted',
            field=models.IntegerField(null=True, choices=[(b'0', b'No'), (b'1', b'Yes')]),
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
