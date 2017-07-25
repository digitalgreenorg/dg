# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0016_auto_20170628_0555'),
    ]

    operations = [
        migrations.CreateModel(
            name='MandiType',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('mandi_type_name', models.CharField(max_length=100)),
                ('mandi_category', models.IntegerField(default=0, choices=[(0, b'Wholesale Market'), (1, b'Retail Market'), (2, b'Individual Entity')])),
                ('type_description', models.CharField(max_length=300, null=True)),
                ('user_created', models.ForeignKey(related_name='loop_manditype_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_manditype_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='mandi',
            name='mandi_type',
            field=models.ForeignKey(default=None, to='loop.MandiType', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='manditype',
            unique_together=set([('mandi_type_name', 'mandi_category')]),
        ),
    ]
