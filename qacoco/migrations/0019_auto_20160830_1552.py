# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0018_auto_20160830_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videocontentapproval',
            name='suitable_for',
            field=models.CharField(max_length=1, choices=[(b'0', b'Not For Adoption'), (b'1', b'For Adoption')]),
        ),
    ]
