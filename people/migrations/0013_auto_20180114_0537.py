# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0006_auto_20180114_0135'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0012_ap_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='AP_Animator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('animator_code', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=255, null=True, blank=True)),
                ('animator', models.ForeignKey(blank=True, to='people.Animator', null=True)),
            ],
            options={
                'verbose_name': 'AP Animator',
                'verbose_name_plural': 'AP Animator',
            },
        ),
        migrations.CreateModel(
            name='AP_AnimatorAssignedVillage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('animator', models.ForeignKey(to='people.AP_Animator')),
                ('user_created', models.ForeignKey(related_name='people_ap_animatorassignedvillage_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='people_ap_animatorassignedvillage_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('village', models.ForeignKey(to='geographies.AP_Village')),
            ],
            options={
                'verbose_name': 'AP AnimatorAssignedVillage',
                'verbose_name_plural': 'AP AnimatorAssignedVillage',
            },
        ),
        migrations.AddField(
            model_name='ap_animator',
            name='assigned_villages',
            field=models.ManyToManyField(related_name='ap_assigned_villages', through='people.AP_AnimatorAssignedVillage', to='geographies.AP_Village', blank=True),
        ),
        migrations.AddField(
            model_name='ap_animator',
            name='user_created',
            field=models.ForeignKey(related_name='people_ap_animator_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ap_animator',
            name='user_modified',
            field=models.ForeignKey(related_name='people_ap_animator_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
