# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geographies', '0007_auto_20180530_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='AP_COCO_Mapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('geo_type', models.CharField(max_length=25)),
                ('ap_geo_id', models.PositiveIntegerField()),
                ('coco_geo_id', models.PositiveIntegerField()),
                ('processed', models.BooleanField(default=False)),
                ('user_created', models.ForeignKey(related_name='geographies_ap_coco_mapping_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='geographies_ap_coco_mapping_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'AP_COCO_Mapping',
                'verbose_name_plural': 'AP_COCO_Mapping',
            },
        ),
        migrations.AddField(
            model_name='ap_district',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ap_mandal',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ap_village',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='block',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='country',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='district',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='jslps_block',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='jslps_district',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='jslps_village',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='state',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='village',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='ap_coco_mapping',
            unique_together=set([('geo_type', 'ap_geo_id', 'coco_geo_id')]),
        ),
    ]
