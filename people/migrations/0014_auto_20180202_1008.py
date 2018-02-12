# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0013_auto_20180114_0537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ap_animator',
            name='animator',
        ),
        migrations.RemoveField(
            model_name='ap_animator',
            name='assigned_villages',
        ),
        migrations.RemoveField(
            model_name='ap_animator',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='ap_animator',
            name='user_modified',
        ),
        migrations.RemoveField(
            model_name='ap_animatorassignedvillage',
            name='animator',
        ),
        migrations.RemoveField(
            model_name='ap_animatorassignedvillage',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='ap_animatorassignedvillage',
            name='user_modified',
        ),
        migrations.RemoveField(
            model_name='ap_animatorassignedvillage',
            name='village',
        ),
        migrations.RemoveField(
            model_name='ap_person',
            name='habitation',
        ),
        migrations.RemoveField(
            model_name='ap_person',
            name='person',
        ),
        migrations.RemoveField(
            model_name='ap_person',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='ap_person',
            name='user_modified',
        ),
        migrations.DeleteModel(
            name='AP_Animator',
        ),
        migrations.DeleteModel(
            name='AP_AnimatorAssignedVillage',
        ),
        migrations.DeleteModel(
            name='AP_Person',
        ),
    ]
