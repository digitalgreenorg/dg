# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0020_auto_20231005_0818'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0023_language_countries'),
        ('activities', '0018_auto_20180410_0849'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerFeedback',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('video_relevance', models.CharField(help_text=b'How relevant was the video?', max_length=20, choices=[(b'relevant', b'Relevant to a great extent'), (b'relevant_to_som_extnt', b'Relevant to some extent'), (b'not_relevant', b'Not Relevant')])),
                ('adoption_confidence', models.BooleanField(help_text=b'Does the farmer feel confident in adopting the practice?')),
                ('non_adoption_reasons', models.CharField(blank=True, max_length=2, null=True, help_text=b'If No, Why?', choices=[(b'a', b'Since I am not clear and convinced in the importance of the technology'), (b'b', b'The input/technology/service for the recommended practice is not easily accessible'), (b'c', b'The cost of the recommended practice is not affordable, and there is no credit facility in our kebele'), (b'd', b'The risk of the investment in the recommended practice is not acceptable'), (b'e', b'Unavailability of Inputs at the Market'), (b'f', b"The technology needs human power and I don't have that"), (b'g', b'The time has passed to adopt the technology'), (b'h', b'My spouse is the one who makes the decision'), (b'i', b'The DA/Mediator will not provide support after dissemination'), (b'j', b'Other (Please specify)')])),
                ('non_adoption_reasons_other', models.TextField(help_text=b'If not confident, reasons for not adopting (e.g., clarity, accessibility, cost, risk, etc.)', null=True, blank=True)),
                ('location_convenience', models.CharField(help_text=b'Feedback on the dissemination location', max_length=20, choices=[(b'safe', b'Safe and convenient'), (b'too_far', b'Too far from my house'), (b'isolated', b'Isolated / not safe to come alone'), (b'other', b'Other')])),
                ('location_convenience_other', models.TextField(help_text=b'Additional details about location convenience', null=True, blank=True)),
                ('time_convenience', models.BooleanField(help_text=b'Was the screening time convenient?')),
                ('convenient_time', models.CharField(blank=True, max_length=20, null=True, help_text=b'If the screening time was not convenient, which alternative time is preferred?', choices=[(b'early_morning', b'Early in the Morning'), (b'mid_day', b'Mid Day'), (b'afternoon', b'In the Afternoon'), (b'late_afternoon', b'Late in the Afternoon'), (b'evening', b'In the Evening')])),
                ('additional_challenges_encountered', models.BooleanField(help_text=b'Do you face any additional challenges in attending video dissemination sessions other than time and location?')),
                ('additional_challenges', models.CharField(blank=True, max_length=20, null=True, help_text=b'If yes, what are the potential problems?', choices=[(b'a', b'My husband is not willing to send me for such events'), (b'b', b'Busy with household chores and social/family issues'), (b'c', b'Mostly the dissemination schedules have been organized in Market days'), (b'd', b"I don't have information about the dissemination schedules"), (b'e', b'Have no one to take care of my children'), (b'f', b'Other (Please specify)')])),
                ('additional_challenges_other', models.TextField(help_text=b'Additional details for challenges encountered', null=True, blank=True)),
                ('comfortable_asking', models.BooleanField(help_text=b'Did the farmer feel comfortable asking questions and participating?')),
                ('asking_discomfort_reasons', models.CharField(blank=True, max_length=2, null=True, help_text=b'If not comfortable, what were the reasons?', choices=[(b'a', b'The DA/Mediator was not encouraging to ask questions'), (b'b', b'The DA/Mediator was only focusing on Model Farmers'), (b'c', b'The DA/Mediator was not encouraging Female Farmers'), (b'd', b'I feel comfortable with Female only group (Female farmers)'), (b'e', b'I am not clear with the topic'), (b'f', b'The topic is not relevant for me'), (b'g', b'The topic is not seasonal'), (b'h', b"I don't have the listed resources to adopt the technology"), (b'i', b'There is not enough time allocated for discussion'), (b'j', b'Other (Please specify)')])),
                ('asking_discomfort_reasons_other', models.TextField(help_text=b'If not comfortable, please specify other reasons', null=True, blank=True)),
                ('recommendation_rating', models.PositiveIntegerField(help_text=b'On a scale of 0-10, how likely is the farmer to recommend the practice?', validators=[django.core.validators.MaxValueValidator(10)])),
                ('nng_recall', models.CharField(help_text=b"Farmer's recall of the main (non-negotiable) points in the video", max_length=20, choices=[(b'all', b'Recalled all NNGs'), (b'partial', b'Recalled partially'), (b'none', b'Did not recall')])),
                ('suggestions', models.TextField(help_text=b'Other agricultural practices or topics the farmer would like to see in videos', null=True, blank=True)),
                ('person', models.ForeignKey(help_text=b'The farmer providing the feedback', to='people.Person')),
                ('screening', models.ForeignKey(help_text=b'The dissemination session this feedback relates to', to='activities.Screening')),
                ('user_created', models.ForeignKey(related_name='activities_farmerfeedback_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='activities_farmerfeedback_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('video', models.ForeignKey(help_text=b'The video shown during the session', to='videos.Video')),
            ],
            options={
                'verbose_name': 'Farmer Feedback',
                'verbose_name_plural': 'Farmer Feedbacks',
            },
        ),
        migrations.AlterUniqueTogether(
            name='farmerfeedback',
            unique_together=set([('screening', 'person', 'video')]),
        ),
    ]
