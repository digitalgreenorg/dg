# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='key_res_content',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Key Resonsibility Content'),
        ),
    ]
