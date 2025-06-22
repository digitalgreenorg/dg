# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0019_auto_20250416_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerfeedback',
            name='additional_challenges',
            field=mezzanine.core.fields.MultiChoiceField(blank=True, max_length=255, null=True, help_text=b'If yes, what are the potential problems?', choices=[(b'a', b'My husband is not willing to send me for such events'), (b'b', b'Busy with household chores and social/family issues'), (b'c', b'Mostly the dissemination schedules have been organized in Market days'), (b'd', b"I don't have information about the dissemination schedules"), (b'e', b'Have no one to take care of my children'), (b'f', b'Other (Please specify)')]),
        ),
        migrations.AlterField(
            model_name='farmerfeedback',
            name='asking_discomfort_reasons',
            field=mezzanine.core.fields.MultiChoiceField(blank=True, max_length=255, null=True, help_text=b'If not comfortable, what were the reasons?', choices=[(b'a', b'The DA/Mediator was not encouraging to ask questions'), (b'b', b'The DA/Mediator was only focusing on Model Farmers'), (b'c', b'The DA/Mediator was not encouraging Female Farmers'), (b'd', b'I feel comfortable with Female only group (Female farmers)'), (b'e', b'I am not clear with the topic'), (b'f', b'The topic is not relevant for me'), (b'g', b'The topic is not seasonal'), (b'h', b"I don't have the listed resources to adopt the technology"), (b'i', b'There is not enough time allocated for discussion'), (b'j', b'Other (Please specify)')]),
        ),
        migrations.AlterField(
            model_name='farmerfeedback',
            name='convenient_time',
            field=mezzanine.core.fields.MultiChoiceField(blank=True, max_length=255, null=True, help_text=b'If the screening time was not convenient, which alternative time is preferred?', choices=[(b'early_morning', b'Early in the Morning'), (b'mid_day', b'Mid Day'), (b'afternoon', b'In the Afternoon'), (b'late_afternoon', b'Late in the Afternoon'), (b'evening', b'In the Evening')]),
        ),
        migrations.AlterField(
            model_name='farmerfeedback',
            name='non_adoption_reasons',
            field=mezzanine.core.fields.MultiChoiceField(blank=True, max_length=255, null=True, help_text=b'If No, Why?', choices=[(b'a', b'Since I am not clear and convinced in the importance of the technology'), (b'b', b'The input/technology/service for the recommended practice is not easily accessible'), (b'c', b'The cost of the recommended practice is not affordable, and there is no credit facility in our kebele'), (b'd', b'The risk of the investment in the recommended practice is not acceptable'), (b'e', b'Unavailability of Inputs at the Market'), (b'f', b"The technology needs human power and I don't have that"), (b'g', b'The time has passed to adopt the technology'), (b'h', b'My spouse is the one who makes the decision'), (b'i', b'The DA/Mediator will not provide support after dissemination'), (b'j', b'Other (Please specify)')]),
        ),
    ]
